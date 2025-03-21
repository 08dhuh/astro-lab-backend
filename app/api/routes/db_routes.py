from fastapi import APIRouter, Depends, HTTPException, Request
from app.services.db_service import *
#from app.services.isochrone_service import isochrone_data

router = APIRouter()


@router.get("/db-status")
def db_status():
    return check_database_status()

@router.get("/isochrone/")
def api_get_isochrone(log_age: float, Z:float, request: Request):
    return query_isochrone(log_age=log_age, Z=Z, app=request.app)


@router.get("/debug/clusters")
def api_get_all_clusters():
    clusters = get_all_clusters()
    return clusters


@router.get("/debug/cluster-ubvs")
def api_get_all_cluster_ubvs():
    cluster_ubvs = get_all_cluster_UBVS()
    return cluster_ubvs


@router.get("/debug/isochrones")
def api_get_isochrones(limit: int = -1):
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
