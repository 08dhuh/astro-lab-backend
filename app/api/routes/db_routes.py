from fastapi import APIRouter, Depends, HTTPException
from app.services.db_service import *

router = APIRouter()


@router.get("/db-status")
def db_status():
    return check_database_status()


@router.get("/debug/clusters")
def api_get_all_clusters():
    clusters = get_all_clusters()
    return clusters


@router.get("/debug/cluster-ubvs")
def api_get_all_cluster_ubvs():
    cluster_ubvs = get_all_cluster_UBVS()
    return cluster_ubvs


@router.get("/debug/isochrones")
def api_get_isochrones(limit: int = 100):
    isochrones = get_isochrones(limit=limit)
    return isochrones


@router.get("/debug/cluster-ubvs/{cluster_id}")
def api_get_cluster_ubv(cluster_id: int):
    ubv_data = get_cluster_ubv(cluster_id)
    if ubv_data is None:
        raise HTTPException(
            status_code=404, detail=f"Cluster not found for {cluster_id}")
    return ubv_data


# @router.get("/debug/clusters-missing")
# def api_get_missing_cluster_pks():
#     missing_pks = find_missing_cluster_pks()
#     return {
#         "missing_count": len(missing_pks),
#         "missing_cluster_pks": missing_pks
#     }
