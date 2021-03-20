.. _interface:

===============
路由接口说明
===============

- API 的路由返回的数据为 JSON 格式
- 使用 GET 或者 Websocket 获取数据
- 使用 POST 动态修改引擎启用状态

视频相关接口
===================

GET /anime/search/<keyword>
""""""""""""""""""""""""""""""""""""
视频搜索接口, 该接口阻塞至所有引擎处理完成, 返回全部搜索结果

==========  ==========  ==========
参数          类型           备注
==========  ==========  ==========
keyword        str          关键词
==========  ==========  ==========

返回值:

.. code-block:: json

    [
        {
            "category": "热血,奇幻",
            "cover_url": "https://img9.doubanio.com/view/photo/m/public/p2578234476.jpg",
            "description": "",
            "module": "api.anime.bimibimi",
            "score": 80,
            "title": "凡人修仙传",
            "url": "http://localhost:6001/anime/62696d6962696d697c313730"
        },
        {
            "category": "动漫",
            "cover_url": "https://ae01.alicdn.com/kf/Udadf545b192247c9988db45344177cd7e.jpg",
            "description": "平凡少年韩立出生贫困，为了让家人过上更好的生活，自愿前去七玄门参加入门考核，最终被墨大夫收入门下墨大...",
            "module": "api.anime.k1080",
            "score": 80,
            "title": "凡人修仙传",
            "url": "http://localhost:6001/anime/6b313038307c2f766f6464657461696c2f3338373736332e68746d6c"
        },
        {
            "category": "奇幻 玄幻",
            "cover_url": "http://sc02.alicdn.com/kf/H72ad113e1a8d43758724d7c1eda50557n.jpg",
            "description": "凡人出身的青年韩立为求大道，纵横人、灵、仙三界，掌握力量，惩恶扬善，快意恩仇的旅程。描绘了一个宏大严谨的仙侠世界，以充满想象力的情节，代入感极强的人物，跌宕起伏的故事，成为当代中国仙侠文学当仁不让的国民级IP。",
            "module": "api.anime.agefans",
            "score": 80,
            "title": "凡人修仙传",
            "url": "http://localhost:6001/anime/61676566616e737c3230323030323833"
        }
    ]

- `score` 字段是对于资源质量的评分，目前暂未实现。
- `module` 字段表明了资源的来源引擎，后续会调度该引擎完成下一步的解析工作。
- `url` 字段的链接指向资源的播放列表信息，访问时才会解析，解析结果会被缓存。

WS  /anime/search
"""""""""""""""""""""""""""""""""""""
异步视频搜索接口, 通过 Websocket 即时推送搜索结果

Web 端:

.. code-block:: javascript

    function search(keyword) {
        let ws = new WebSocket("ws://localhost:6001/anime/search");

        ws.onopen = function (evt) {
            console.log("Connection open ...");
            ws.send(keyword);
        };

        ws.onmessage = function (evt) {
            let data = JSON.parse(evt.data);
            console.log(`Received Message: ${JSON.stringify(data)}`);
        };

        ws.onclose = function (evt) {
            console.log("Connection closed.");
        };
    }


.. code-block:: javascript

    search("凡人修仙传")

当某一个引擎搜索到数据，将立即推送给前端:

.. code-block::

    Connection open ...
    Received Message: {"category":"热血,奇幻","cover_url":"https://img9.doubanio.com/view/photo/m/public/p2578234476.jpg","description":"","engine":"api.anime.bimibimi","score":80,"title":"凡人修仙传","url":"http://localhost:6001/anime/62696d6962696d697c313730"}
    Received Message: {"category":"动漫","cover_url":"https://ae01.alicdn.com/kf/Udadf545b192247c9988db45344177cd7e.jpg","description":"平凡少年韩立出生贫困，为了让家人过上更好的生活，自愿前去七玄门参加入门考核，最终被墨大夫收入门下墨大...","engine":"api.anime.k1080","score":80,"title":"凡人修仙传","url":"http://localhost:6001/anime/6b313038307c2f766f6464657461696c2f3338373736332e68746d6c"}
    Received Message: {"category":"奇幻 玄幻","cover_url":"http://sc02.alicdn.com/kf/H72ad113e1a8d43758724d7c1eda50557n.jpg","description":"凡人出身的青年韩立为求大道，纵横人、灵、仙三界，掌握力量，惩恶扬善，快意恩仇的旅程。描绘了一个宏大严谨的仙侠世界，以充满想象力的情节，代入感极强的人物，跌宕起伏的故事，成为当代中国仙侠文学当仁不让的国民级IP。","engine":"api.anime.agefans","score":80,"title":"凡人修仙传","url":"http://localhost:6001/anime/61676566616e737c3230323030323833"}
    Connection closed.


GET /anime/<token>
""""""""""""""""""""""""""""""""
剧集详情接口, 返回播放列表等信息

==========  ==========  ==========
参数          类型           备注
==========  ==========  ==========
token        str        播放列表的唯一标识
==========  ==========  ==========

返回值(结果过多已省略):

.. code-block:: json

    {
        "title": "凡人修仙传",
        "category": "动漫",
        "cover_url": "https://ae01.alicdn.com/kf/Uba0447ef35b64eb59a3b4793cae384c6i.jpg",
        "description": "平凡少年韩立出生贫困，为了让家人过上更好的生活，自愿前去七玄门参加入门考核，最终...",
        "module": "api.anime.k1080",
        "play_lists": [
            {
                "name": "超清推荐",
                "num": 20,
                "video_list": [
                    {
                        "info": "http://localhost:6001/anime/6b313038307c2f766f6464657461696c2f3338373736332e68746d6c/0/0",
                        "name": "01",
                        "player": "http://localhost:6001/anime/6b313038307c2f766f6464657461696c2f3338373736332e68746d6c/0/0/player"
                    },
                    {
                        "info": "http://localhost:6001/anime/6b313038307c2f766f6464657461696c2f3338373736332e68746d6c/0/1",
                        "name": "02",
                        "player": "http://localhost:6001/anime/6b313038307c2f766f6464657461696c2f3338373736332e68746d6c/0/1/player"
                    },
                    {
                        "info": "http://localhost:6001/anime/6b313038307c2f766f6464657461696c2f3338373736332e68746d6c/0/2",
                        "name": "03",
                        "player": "http://localhost:6001/anime/6b313038307c2f766f6464657461696c2f3338373736332e68746d6c/0/2/player"
                    }
                ]
            },
            {
                "name": "ok",
                "num": 20,
                "video_list": [
                    {
                        "info": "http://localhost:6001/anime/6b313038307c2f766f6464657461696c2f3338373736332e68746d6c/1/0",
                        "name": "第01集",
                        "player": "http://localhost:6001/anime/6b313038307c2f766f6464657461696c2f3338373736332e68746d6c/1/0/player"
                    },
                    {
                        "info": "http://localhost:6001/anime/6b313038307c2f766f6464657461696c2f3338373736332e68746d6c/1/1",
                        "name": "第02集",
                        "player": "http://localhost:6001/anime/6b313038307c2f766f6464657461696c2f3338373736332e68746d6c/1/1/player"
                    }
                ]
            }
        ]
    }

- `play_lists` 中可能包含多个播放列表(路线)。
- `player` 字段是播放器地址(无弹幕)，用于测试视频直链或者代理功能是否正常。
- `info` 字段的链接指向视频的详细详细，访问时才解析，解析结果会被缓存。

GET /anime/<token>/<playlist>/<episode>
"""""""""""""""""""""""""""""""""""""""""""""""""
获取某一集视频的详细信息

==========  ==========  ==========
参数          类型           备注
==========  ==========  ==========
token        str        资源token
playlist     int        播放列表编号
episode      int        视频集数编号
==========  ==========  ==========

返回值:

.. code-block:: json

    {
        "format": "mp4",
        "lifetime": 86399,
        "proxy_url": "http://localhost:6001/proxy/stream/6b313038307c2f766f6464657461696c2f3338373736332e68746d6c/0/0",
        "raw_url": "http://localhost:6001/anime/6b313038307c2f766f6464657461696c2f3338373736332e68746d6c/0/0/url",
        "resolution": "1280x720",
        "size": 919586946
    }

- `format` 字段是根据 URL 和 Content-Type 推断出来的视频格式
  (未启用 `Magic Number <https://en.wikipedia.org/wiki/Magic_number_(programming)>`_ 推导视频格式)。
- `lifetime` 字段是用户解析直链时设置的直链有效期，单位为秒。若用户没有设置直链有效期， API 将从 URL 中寻找一个有效的时间戳
  来推断直链生命周期，如果推断失败，则默认直链有效期为一天。
- `raw_url` 字段是视频的直链，这里给出的值是 API 的一个路由地址，它会动态地重定向到视频的直链(当缓存的直链过期时，重新解析并重定向)
- `proxy_url` 字段是代理 URL 地址，可作为视频直链使用。当视频存在防盗链时，API 作为代理服务器转发视频数据流。如果视频为 `HLS` ( `m3u8` )
  格式，该接口将重定向到原始直链(通常提供 `HLS` 视频的服务器支持 CORS，而对于 `HLS` 流媒体的代理十分复杂，暂未实现)
- `resolution` 字段是从 `MPEG-TS <https://en.wikipedia.org/wiki/MPEG_transport_stream>`_ /
  `MPEG-4 <https://en.wikipedia.org/wiki/MPEG-4>`_ 流的元数据中推断出来的视频分辨率，目前暂未完整实现。
- `size` 字段为视频的字节大小，对于 `m3u8` 视频的大小推断暂不准确。

GET /anime/bangumi/updates
""""""""""""""""""""""""""""""""""""""""""""""""""""""
番组表接口, 获取最近一段时间更新的番剧信息

返回值(结果过多已省略):

.. code-block:: json

    [
        {
            "date": "2021-02-16",
            "day_of_week": "2",
            "is_today": false,
            "updates": [
                {
                    "cover_url": "http://i0.hdslb.com/bfs/bangumi/image/8d1be9e8c77696f34886b8f471d935f504a014d3.jpg",
                    "title": "天官赐福",
                    "update_time": "2021-02-16 11:00:00",
                    "update_to": "特别篇"
                }
            ]
        },
        {
            "date": "2021-02-17",
            "day_of_week": "3",
            "is_today": false,
            "updates": [
                {
                    "cover_url": "http://i0.hdslb.com/bfs/bangumi/image/a4ca27f00b7ad3f319e04723ee29a3a1a435e666.jpg",
                    "title": "阿衰 第四季",
                    "update_time": "2021-02-17 20:00:00",
                    "update_to": "第1话-第3话"
                }
            ]
        }
    ]

- 番组表大概有一个月的数据
- `day_of_week` 字段表示当前星期几
- `is_today` 字段表示是否是今天的数据
- `update_time` 字段为番剧的更新时间
- `update_to` 字段为最新一话的内容

-------------------------------------------------

弹幕相关接口
=====================

GET /danmaku/search/<keyword>
""""""""""""""""""""""""""""""""""""""""""""""
弹幕搜索接口, 阻塞至所有引擎处理完成, 返回全部结果

==========  ==========  ==========
参数          类型           备注
==========  ==========  ==========
keyword        str          关键词
==========  ==========  ==========

返回值:

.. code-block:: json

    [
        {
            "module": "api.danmaku.bilibili",
            "num": 6,
            "score": 80,
            "title": "Re：从零开始的异世界生活 第二季 后半",
            "url": "http://localhost:6001/danmaku/62696c6962696c697c2f62616e67756d692f706c61792f737333363432392f"
        },
        {
            "module": "api.danmaku.bilibili",
            "num": 13,
            "score": 80,
            "title": "Re：从零开始的异世界生活 第二季 前半",
            "url": "http://localhost:6001/danmaku/62696c6962696c697c2f62616e67756d692f706c61792f737333333830322f"
        },
        {
            "module": "api.danmaku.tencent",
            "num": 19,
            "score": 80,
            "title": "Re:从零开始的异世界生活 第2季",
            "url": "http://localhost:6001/danmaku/74656e63656e747c6d7a63303032303063386b306c7a31"
        }
    ]

- 搜索一次视频，在不同的搜索结果间切换时搜索弹幕库使用的关键词往往相同，所以弹幕搜索结果会被缓存。
- `num` 字段表示弹幕播放列表的集数，`-1` 表示解析前无法获取数量信息。
- `score` 字段是对于资源的质量的评分，目前暂未实现。
- `url` 字段指向该弹幕播放列表的详细信息，访问时解析，解析结果会被缓存。

WS  /danmaku/search
"""""""""""""""""""""""""""""""""
异步弹幕搜索接口, 通过 Websocket 即时推送搜索结果

Web 端:

.. code-block:: javascript

    function search(keyword) {
        let ws = new WebSocket("ws://localhost:6001/danmaku/search");

        ws.onopen = function (evt) {
            console.log("Connection open ...");
            ws.send(keyword);
        };

        ws.onmessage = function (evt) {
            let data = JSON.parse(evt.data);
            console.log(`Received Message: ${JSON.stringify(data)}`);
        };

        ws.onclose = function (evt) {
            console.log("Connection closed.");
        };
    }


.. code-block:: javascript

    search("进击的巨人")

当某一个引擎搜索到数据，将立即推送给前端:

.. code-block::

    Connection open ...
    Received Message: {"module":"api.danmaku.bahamut","num":9,"score":80,"title":"进击的巨人 The Final Season","url":"http://localhost:6001/danmaku/626168616d75747c616e696d655265662e7068703f736e3d313132353232"}
    Received Message: {"module":"api.danmaku.bahamut","num":25,"score":80,"title":"进击的巨人","url":"http://localhost:6001/danmaku/626168616d75747c616e696d655265662e7068703f736e3d3539323231"}
    Received Message: {"module":"api.danmaku.bahamut","num":23,"score":80,"title":"进击的巨人 第三季","url":"http://localhost:6001/danmaku/626168616d75747c616e696d655265662e7068703f736e3d3839353537"}
    Received Message: {"module":"api.danmaku.bahamut","num":17,"score":80,"title":"进击的巨人 第二季","url":"http://localhost:6001/danmaku/626168616d75747c616e696d655265662e7068703f736e3d3732373535"}
    Received Message: {"module":"api.danmaku.bahamut","num":1,"score":80,"title":"进击的巨人 剧场版 CHRONICLE","url":"http://localhost:6001/danmaku/626168616d75747c616e696d655265662e7068703f736e3d313131363532"}
    Received Message: {"module":"api.danmaku.bahamut","num":1,"score":80,"title":"剧场版 进击的巨人 觉醒的咆哮","url":"http://localhost:6001/danmaku/626168616d75747c616e696d655265662e7068703f736e3d3932323735"}
    Received Message: {"module":"api.danmaku.bahamut","num":1,"score":80,"title":"剧场版 进击的巨人 前编 红莲的弓矢","url":"http://localhost:6001/danmaku/626168616d75747c616e696d655265662e7068703f736e3d3638373531"}
    Received Message: {"module":"api.danmaku.bahamut","num":1,"score":80,"title":"剧场版 进击的巨人 后编 自由之翼","url":"http://localhost:6001/danmaku/626168616d75747c616e696d655265662e7068703f736e3d3638373532"}
    Received Message: {"module":"api.danmaku.bilibili","num":12,"score":80,"title":"進擊的巨人 第二季（僅限台灣地區）","url":"http://localhost:6001/danmaku/62696c6962696c697c2f62616e67756d692f706c61792f7373353937302f"}
    Received Message: {"module":"api.danmaku.bilibili","num":10,"score":80,"title":"進擊的巨人 第三季 Part.2（僅限台灣地區）","url":"http://localhost:6001/danmaku/62696c6962696c697c2f62616e67756d692f706c61792f737332363936332f"}
    Received Message: {"module":"api.danmaku.bilibili","num":12,"score":80,"title":"進擊的巨人 第三季（僅限台灣地區）","url":"http://localhost:6001/danmaku/62696c6962696c697c2f62616e67756d692f706c61792f737332343632392f"}
    Connection closed.


GET /danmaku/<token>
""""""""""""""""""""""""""""""""""""
弹幕详情接口, 返回弹幕播放列表

==========  ==========  ==========
参数          类型           备注
==========  ==========  ==========
token        str         该弹幕列表的唯一标识
==========  ==========  ==========

返回值:

.. code-block:: json

    [
        {
            "data": "http://localhost:6001/danmaku/626168616d75747c616e696d655265662e7068703f736e3d313132353232/0/v3/",
            "name": "1",
            "url": "http://localhost:6001/danmaku/626168616d75747c616e696d655265662e7068703f736e3d313132353232/0"
        },
        {
            "data": "http://localhost:6001/danmaku/626168616d75747c616e696d655265662e7068703f736e3d313132353232/1/v3/",
            "name": "2",
            "url": "http://localhost:6001/danmaku/626168616d75747c616e696d655265662e7068703f736e3d313132353232/1"
        },
        {
            "data": "http://localhost:6001/danmaku/626168616d75747c616e696d655265662e7068703f736e3d313132353232/2/v3/",
            "name": "3",
            "url": "http://localhost:6001/danmaku/626168616d75747c616e696d655265662e7068703f736e3d313132353232/2"
        },
        {
            "data": "http://localhost:6001/danmaku/626168616d75747c616e696d655265662e7068703f736e3d313132353232/3/v3/",
            "name": "4",
            "url": "http://localhost:6001/danmaku/626168616d75747c616e696d655265662e7068703f736e3d313132353232/3"
        },
        {
            "data": "http://localhost:6001/danmaku/626168616d75747c616e696d655265662e7068703f736e3d313132353232/4/v3/",
            "name": "5",
            "url": "http://localhost:6001/danmaku/626168616d75747c616e696d655265662e7068703f736e3d313132353232/4"
        },
        {
            "data": "http://localhost:6001/danmaku/626168616d75747c616e696d655265662e7068703f736e3d313132353232/5/v3/",
            "name": "6",
            "url": "http://localhost:6001/danmaku/626168616d75747c616e696d655265662e7068703f736e3d313132353232/5"
        },
        {
            "data": "http://localhost:6001/danmaku/626168616d75747c616e696d655265662e7068703f736e3d313132353232/6/v3/",
            "name": "7",
            "url": "http://localhost:6001/danmaku/626168616d75747c616e696d655265662e7068703f736e3d313132353232/6"
        },
        {
            "data": "http://localhost:6001/danmaku/626168616d75747c616e696d655265662e7068703f736e3d313132353232/7/v3/",
            "name": "8",
            "url": "http://localhost:6001/danmaku/626168616d75747c616e696d655265662e7068703f736e3d313132353232/7"
        },
        {
            "data": "http://localhost:6001/danmaku/626168616d75747c616e696d655265662e7068703f736e3d313132353232/8/v3/",
            "name": "9",
            "url": "http://localhost:6001/danmaku/626168616d75747c616e696d655265662e7068703f736e3d313132353232/8"
        }
    ]

- `url` 字段填入 `Dplayer` 作为弹幕地址
- `data` 字段用于测试, 返回弹幕池数据(`DPlayer` 会自动在 `url` 后面加上 `/v3/` )

Dplayer `配置 <https://dplayer.js.org/zh/guide.html#%E5%BC%B9%E5%B9%95%E6%8E%A5%E5%8F%A3>`_:

.. code-block:: javascript

    const option = {
        danmaku: {
            addition: ['http://localhost:6001/danmaku/626168616d75747c616e696d655265662e7068703f736e3d313132353232/8']
        }
    };

GET /danmaku/<token>/<episode>/v3/
""""""""""""""""""""""""""""""""""""""""
弹幕数据接口, 返回一集视频的弹幕( `Dplayer` 格式)

==========  ==========  ==========
参数          类型           备注
==========  ==========  ==========
token        str         弹幕播放列表唯一标识
episode      int         弹幕集数编号
==========  ==========  ==========

返回值(结果过多已省略):

.. code-block:: json

    {
        "code": 0,
        "num": 2785,
        "data": [
            [0, 0, 16777215, "", "天啊 迟到了"],
            [0, 0, 16777215, "", "ㄢㄢ"],
            [0, 0, 16777215, "", "二刷"],
            [0, 2, 16711718, "", "终于"],
            [0, 0, 16777215, "", "0"],
            [0, 0, 16777215, "", "主席好"],
            [0, 0, 16639293, "", "终于来看第四季了啦"],
            [0, 0, 16750117, "", "进击的观众！"],
            [0, 1, 16711718, "", "以三刷"],
            [0, 1, 16711718, "", "以2刷"],
            [0, 0, 16777215, "", "😏"],
            [0, 0, 16777215, "", "赞喔！"]
        ]
    }

- `num` 字段表弹幕条数
- 弹幕格式为: `[time, pos, color, user, message]` ,
  `time` 距离视频开头的秒数(float),
  `pos` 位置参数(0右边, 1上边, 2底部),
  `color` 颜色码 10 进制,
  `user` 发送弹幕的用户名,
  `message` 为弹幕正文内容,

---------------------------------------------

漫画相关接口
===================
暂无，敬请期待~

---------------------------------------------

小说相关接口
=====================
暂无，敬请期待~

---------------------------------------------

音乐相关接口
========================
暂无，敬请期待~

---------------------------------------------

IPTV相关接口
==============

GET /iptv/list
"""""""""""""""""""""""""
获取 IPTV 源列表

返回值(结果过多已省略):

.. code-block:: json

    [
        {
            "name": "CCTV-10科教",
            "url": "http://ivi.bupt.edu.cn/hls/cctv10.m3u8"
        },
        {
            "name": "CCTV-11戏曲",
            "url": "http://ivi.bupt.edu.cn/hls/cctv11.m3u8"
        },
        {
            "name": "CCTV-12社会与法",
            "url": "http://ivi.bupt.edu.cn/hls/cctv12.m3u8"
        },
        {
            "name": "CCTV-13新闻",
            "url": "http://ivi.bupt.edu.cn/hls/cctv13.m3u8"
        },
        {
            "name": "CCTV-14少儿",
            "url": "http://ivi.bupt.edu.cn/hls/cctv14.m3u8"
        }
    ]

- 目前只有国内地方卫视台和 CCTV
- 更多来源等待添加

---------------------------------------------

代理相关接口
===============

GET /proxy/image/<url>
""""""""""""""""""""""""""""""""
代理访问跨域的图片资源

==========  ==========  ==========
参数          类型           备注
==========  ==========  ==========
url           str         目标 URL
==========  ==========  ==========

如果直接访问图片出现跨域问题, 可通过此接口代理访问, 接口原样转发服务器的响应。

GET /proxy/stream/<token>/<playlist>/<episode>
""""""""""""""""""""""""""""""""""""""""""""""""""""""""
代理普通视频数据流, 用于解决防盗链和跨域问题

==========  ==========  ==========
参数          类型           备注
==========  ==========  ==========
token        str        资源token
playlist     int        播放列表编号
episode      int        视频集数编号
==========  ==========  ==========

使用用户定义的 `Headers` 访问原始资源, 根据请求中 `Range` 字段返回指定位置的视频数据流。
如果处理过程中直链失效，会自动重新解析。

GET /proxy/hls/<token>/<playlist>/<episode>
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
代理 HLS 视频数据流, 用于解决防盗链和跨域问题

==========  ==========  ==========
参数          类型           备注
==========  ==========  ==========
token        str        资源token
playlist     int        播放列表编号
episode      int        视频集数编号
==========  ==========  ==========

该功能暂未实现：

- 提供 `HLS` 视频的服务器通常支持 CORS
- `HLS` 代理比较复杂，许多站返回的数据格式不规范，或存在自定义的加密手段。

---------------------------------------------

系统相关接口
================

GET /system/logs
""""""""""""""""""""""""""""""
获取 API 的运行日志

GET /system/version
""""""""""""""""""""""""""""""""
获取系统版本信息

返回值:

.. code-block:: json

    {
      "desc": "歪比歪比，歪比巴卜",
      "tag": "1.3.0",
      "time": "2021-02-10",
      "update": "https://gitee.com/api/v5/repos/zaxtyson/AnimeSearcher/releases/latest"
    }

- 由于 `Github` 国内访问速度不妙，所以更新链接使用 `Gitee` 的镜像地址

GET /system/clear
"""""""""""""""""""""""""""""""""
清空 API 解析过程中的缓存

返回值:

.. code-block:: json

    {
        "clear": "success",
        "free": 2244.546875
    }

- `free` 字段为释放的缓存大小，单位 `KB`

GET /system/modules
"""""""""""""""""""""""""""""""""""
获取引擎模块信息

返回值(结果过多已省略):

.. code-block:: json

    {
        "anime": [
            {
                "enable": true,
                "module": "api.anime.agefans",
                "name": "AGE动漫",
                "notes": "少部分资源存在水印，响应速度也不错",
                "quality": 8,
                "type": [
                    "动漫"
                ]
            }
        ],
        "danmaku": [
            {
                "enable": true,
                "module": "api.danmaku.bilibili",
                "name": "哔哩哔哩",
                "notes": "提供B站官方和用户上传番剧的弹幕",
                "quality": 10
            }
        ],
        "comic": [],
        "music": []
    }

POST /system/modules
"""""""""""""""""""""""""""""""""""
启用/停用指定的引擎模块

发送 JSON, 批量修改引擎状态:

.. code-block:: json

    [
        {
            "module": "api.anime.agefans",
            "enable": false
        },
        {
            "module": "api.anime.meijuxia",
            "enable": false
        },
        {
            "module": "api.danmaku.tencent",
            "enable": true
        },
        {
            "module": "api.foo.bar",
            "enable": true
        }
    ]

返回值:

.. code-block:: json

    {
        "api.anime.agefans": "success",
        "api.anime.meijuxia": "success",
        "api.danmaku.tencent": "success",
        "api.foo.bar": "failed"
    }

- 操作成功返回 `success`, 失败返回 `failed`
- 批量操作支持各种引擎的自由搭配
