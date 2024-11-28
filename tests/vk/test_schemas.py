from src.vk.schemas import LikesFirstResponseSchema, LikesRestResponseSchema
from src.vk.scraper import fetch_chunk_likes, parse_id_vk_users


def test_likes_schemas(httpx_mock):

    PAYLOAD_RESPONSE = [
        '<!--{"payload":[0,[false,"<div>123</div>",{"wkRaw":"likes/clip-227618970_456239063","preload":["<div>456</div>", 0, true],"like_obj":"clip-227618970_456239063","offset":60,"tab":"likes","reply_names":[],"wall_opts":{},"type":"likes","width":638,"commonClass":"wk_likes","nocross":true},"n"]],"static":"","statsMeta":{"platform":"web2","st":false,"time":1732209224,"hash":"33GJzuRdbqzsKxFCtcB8KJoUBkLgOuSp4kng03DEpbL","reloadVersion":31},"loaderVersion":"21284103711","pageviewCandidate":true,"langPack":4,"langVersion":"5493","langKeys":{},"templates":{"_":"_"}}',
        '<!--{"payload":[0,[false,"<div>123</div>",{"wkRaw":"likes/clip-227618970_456239063","preload":false,"like_obj":"clip-227618970_456239063","offset":60,"tab":"likes","reply_names":[],"wall_opts":{},"type":"likes","width":638,"commonClass":"wk_likes","nocross":true},"n"]],"static":"","statsMeta":{"platform":"web2","st":false,"time":1732209224,"hash":"33GJzuRdbqzsKxFCtcB8KJoUBkLgOuSp4kng03DEpbL","reloadVersion":31},"loaderVersion":"21284103711","pageviewCandidate":true,"langPack":4,"langVersion":"5493","langKeys":{},"templates":{"_":"_"}}',
        '<!--{"payload":[0,["<div>789</div>",120,true,[],false]],"statsMeta":{"platform":"web2","st":false,"time":1732204116,"hash":"p4lfpdLyhrqgqlAzFyvVHv7PSBBUNN1GLb6Hye7ygmH","reloadVersion":31},"pageviewCandidate":true,"langVersion":"10105"}'
    ]

    for payload in PAYLOAD_RESPONSE:
        httpx_mock.add_response(
            method='POST',
            url='https://vk.com/wkview.php?act=show',
            status_code=200,
            text=payload
        )

    result1 = fetch_chunk_likes('wall-220568323_922')
    assert LikesFirstResponseSchema(**result1).html_content == '<div>456</div><div>123</div>'

    result2 = fetch_chunk_likes('wall-220568323_922')
    assert LikesFirstResponseSchema(**result2).html_content == '<div>123</div>'

    result3 = fetch_chunk_likes('wall-220568323_922')
    assert LikesRestResponseSchema(**result3).html_content == '<div>789</div>'


def test_parse_id_vk_users():
    pass