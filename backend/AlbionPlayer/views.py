import json
from typing import List

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_GET, require_POST

from AOGSbackend.albion.albion_api import AlbionApi
from AOGSbackend.decorators.authenticated_decorator import authenticated
from AOGSbackend.utils.http_tools import error_response
from AlbionPlayer.models import AlbionPlayer


@authenticated
@require_GET
def get_players(request: HttpRequest) -> HttpResponse:
    query_set: QuerySet = AlbionPlayer.objects.filter(user=request.user.user_id)
    players: List[AlbionPlayer] = list(query_set)

    return JsonResponse(players, safe=False)


@authenticated
@require_POST
def add_players(request: HttpRequest) -> HttpResponse:
    name: str = json.loads(request.body).get("player_name")
    if name is None or len(name.strip()) < 1:
        return error_response("Unprocessable Entity", "The player could not be added", 422)
    data = AlbionApi.get_player_by_name(name)
    if data is None:
        return error_response("Unprocessable Entity", "The player could not be added", 422)

    player = AlbionPlayer(player_id=data.id, name=data.name, user=request.user.user_id)
    player.save()
    query_set: QuerySet = AlbionPlayer.objects.filter(user=request.user.user_id)
    players: List[AlbionPlayer] = list(query_set)
    return JsonResponse(players, safe=False)


@authenticated
@require_POST
def remove_players(request: HttpRequest) -> HttpResponse:
    name: str = json.loads(request.body).get("player_name")
    if name is None or len(name.strip()) < 1:
        return error_response("Unprocessable Entity", "The player could not be added", 422)
    data = AlbionApi.get_player_by_name(name)
    if data is None:
        return error_response("Unprocessable Entity", "The player could not be added", 422)
    player = AlbionPlayer.objects.get(player_id=data.id, user=request.user.user_id)
    player.delete()
    query_set: QuerySet = AlbionPlayer.objects.filter(user=request.user.user_id)
    players: List[AlbionPlayer] = list(query_set)
    return JsonResponse(players, safe=False)
