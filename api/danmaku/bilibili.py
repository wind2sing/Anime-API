import re
from json import loads

from api.core.danmaku import *


class BiliBili(DanmakuSearcher):
    """搜索哔哩哔哩官方和用户上传的番剧弹幕"""

    async def get_data_with_params(self, params: dict):
        api = "https://api.bilibili.com/x/web-interface/search/type"
        resp = await self.get(api, params=params)
        if not resp or resp.status != 200:
            return

        data = await resp.json(content_type=None)
        if data["code"] != 0 or data["data"]["numResults"] == 0:
            return

        for item in data["data"]["result"]:
            if '<em class="keyword">' not in item["title"]:  # 没有匹配关键字, 是B站的推广视频
                continue
            if "港澳台" in item["title"]:
                continue  # 港澳台地区弹幕少的可怜
            title = item["title"].replace(r'<em class="keyword">', "").replace("</em>", "")  # 番剧标题
            num = int(item.get("ep_size") or -1)  # 集数, 未知的时候用 -1 表示
            play_num = int(item.get("play") or -1)  # 用户投稿的视频播放数
            play_url = item.get("goto_url") or item.get("arcurl")  # 番剧播放页链接
            play_url = re.sub(r"https?://www.bilibili.com", "", play_url)  # 缩短一些, 只留关键信息
            yield title, num, play_num, play_url

    async def search_from_official(self, params: dict):
        """官方番剧区数据, 全部接收"""
        results = []
        async for item in self.get_data_with_params(params):
            title, num, _, play_url = item
            meta = DanmakuMeta()
            meta.title = title
            meta.play_url = play_url
            meta.num = num
            results.append(meta)
        return results

    async def search_from_users(self, params: dict):
        """用户投稿的番剧, 说不定有好东西"""
        results = []
        async for item in self.get_data_with_params(params):
            title, num, play_num, play_url = item
            if play_num > 100_000:  # 播放量大于 10w 的留着
                meta = DanmakuMeta()
                meta.title = title
                meta.play_url = play_url
                meta.num = num
                results.append(meta)
        return results

    async def search(self, keyword: str):
        params1 = {"keyword": keyword, "search_type": "media_bangumi", "page": 1}  # 搜索番剧
        params2 = {"keyword": keyword, "search_type": "media_ft", "page": 1}  # 搜索影视
        params3 = {"keyword": keyword, "search_type": "video", "tids": 13, "order": "dm",
                   "page": 1, "duration": 4}  # 用户上传的 60 分钟以上的视频, 按弹幕数量排序
        tasks = [
            self.search_from_official(params1),
            self.search_from_official(params2),
            self.search_from_users(params3)
        ]
        async for item in self.as_iter_completed(tasks):
            yield item


class BiliDanmakuDetailParser(DanmakuDetailParser):

    async def parse(self, play_url: str) -> DanmakuDetail:
        detail = DanmakuDetail()
        play_url = "https://www.bilibili.com" + play_url
        resp = await self.get(play_url)
        if not resp or resp.status != 200:
            return detail

        html = await resp.text()
        data_json = re.search(r"window.__INITIAL_STATE__=({.+?\});\(function\(\)", html)
        data_json = loads(data_json.group(1))
        ep_list = data_json.get("epList")  # 官方番剧数据
        if not ep_list and data_json.get("sections"):
            ep_list = data_json["sections"][0]["epList"]  # PV 的数据位置不一样
        if ep_list:  # 官方番剧
            for ep in ep_list:
                danmaku = Danmaku()
                danmaku.name = ep["titleFormat"] + ep["longTitle"]
                danmaku.cid = str(ep["cid"])  # cid 号
                detail.append(danmaku)
            return detail
        # 用户上传的视频
        ep_list = data_json.get("videoData").get("pages")
        for ep in ep_list:  # 用户上传的视频
            danmaku = Danmaku()
            danmaku.name = ep.get("part") or ep.get("from")
            danmaku.cid = str(ep["cid"])  # cid 号
            detail.append(danmaku)
        return detail


class BiliDanmakuDataParser(DanmakuDataParser):

    async def parse(self, cid: str) -> DanmakuData:
        result = DanmakuData()
        api = "https://api.bilibili.com/x/v1/dm/list.so"
        params = {"oid": cid}
        resp = await self.get(api, params)
        if not resp or resp.status != 200:
            return result
        xml_text = await resp.text()
        bullets = re.findall(r'p="(\d+\.?\d*?),\d,\d\d,(\d+?),\d+,(\d),.+?>(.+?)</d>', xml_text)
        for bullet in bullets:
            result.append_bullet(
                time=float(bullet[0]),
                pos=int(bullet[2]),
                color=int(bullet[1]),
                message=bullet[3]
            )
        return result
