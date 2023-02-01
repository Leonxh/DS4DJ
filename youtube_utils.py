from youtubesearchpython.__future__ import VideosSearch


async def get_id_by_name(search_string: str):
    videos_search = VideosSearch(search_string, limit=1)
    videos_result = await videos_search.next()
    return videos_result.get("result")[0].get("id")
