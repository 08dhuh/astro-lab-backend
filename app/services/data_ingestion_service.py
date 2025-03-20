from sqlmodel import Session, select
from stellar_isochrones.isochrones_loader import read_default_isochrones
from stellar_isochrones.zams_loader import load_interpolated_zams
from stellar_isochrones.open_cluster_list_query_process import query_open_cluster_table
from stellar_isochrones.open_cluster_individual_query_process import query_cluster_ubv, find_alternative_dirname
from app.database.models.hr_models import Isochrone, ZAMS, StarCluster, ClusterUBV, engine


def insert_isochrone_data():  # TODO: customise arguments
    try:
        # first check if the isochrone table exists
        with Session(engine) as session:
            existing_entry = session.exec(select(Isochrone)).first()
            if existing_entry:
                print("Isochrone data already exists. Skipping insert.")
                return

            df = read_default_isochrones()
            if df.empty:
                print('invalid dataset')
                return

            iso_records = [
                Isochrone(
                    Z=row["Z"],
                    log_age=row["log_age"],
                    b_v=row["b_v"],
                    Mv=row["Mv"]
                )
                for _, row in df.iterrows()
            ]

            session.add_all(iso_records)
            session.commit()
            print(f"Inserted {len(iso_records)} isochrone records.")
    except Exception as e:
        print(f"Error: {e}")


def insert_zams_data(interporlate=True, num_points=500):
    try:
        with Session(engine) as session:
            # first check if the zams table exists
            existing_entry = session.exec(select(ZAMS)).first()
            if existing_entry:
                print("ZAMS data already exists. Skipping insert.")
                return
            df = load_interpolated_zams(interpolate=interporlate,
                                        num_points=num_points)

            zams_records = [
                ZAMS(
                    b_v=row["b_v"],
                    Mv=row["Mv"]
                )
                for _, row in df.iterrows()
            ]

            session.add_all(zams_records)
            session.commit()
            print(f"Inserted {len(zams_records)} ZAMS records.")
    except Exception as e:
        print(f"Error: {e}")


def insert_star_clusters():
    try:
        with Session(engine) as session:
            # first check if the oc table exists
            existing_entry = session.exec(select(StarCluster)).first()
            if existing_entry:
                print("Open Cluster data already exists. Skipping insert.")
                return

            df = query_open_cluster_table()

            cluster_records = [
                StarCluster(
                    cluster_id=row["id"],
                    name=row["name"],
                    star_count=row["star_count"],
                    reddening=row.get("E(B-V)"),
                    fe_h=row.get("[Fe/H]"),
                    distance_pc=row.get("distance_pc"),
                    log_age=row.get("log_age")
                )
                for _, row in df.iterrows()
            ]
            session.add_all(cluster_records)
            session.commit()
            print(f"Inserted {len(cluster_records)} star cluster records.")
    except Exception as e:
        print(f"Error: {e}")


def insert_cluster_ubv_data():
    try:
        with Session(engine) as session:            
            # first check if the cluster_ubv table exists
            clusters = session.exec(select(StarCluster)).all()
            # skip if the cluster_ubv table is empty
            if not clusters:
                print("No star clusters found. Skipping insert.")
                return
            #check if the cluster_ubv table exists
            total_ubv_count = sorted(set(session.exec(select(ClusterUBV.cluster_pk))))

            if len(total_ubv_count) >= len(clusters):
                print("All clusters already have UBV data. Skipping insert.")
                return
            print(f'{len(clusters) - len(total_ubv_count)} missing cluster ubv data.')

            for cluster in clusters:  # 449 entries
                cluster_id = cluster.cluster_id

                existing_ubv = session.exec(select(ClusterUBV).where(ClusterUBV.cluster_pk == cluster.pk)).all()
                print(existing_ubv)
                existing_ubv_count = len(existing_ubv)

                if existing_ubv_count > 0:
                    print(f"UBV data already exists for cluster {cluster_id}. Skipping to the next")
                    continue  # Skip this cluster and move to the next one

                print(f'fetching ubv for cluster {cluster_id}')

                try:
                    hr_df = query_cluster_ubv(cluster_id)
                    if hr_df.empty: #change this logic
                        alt_cluster_id = find_alternative_dirname(cluster_id)
                        if alt_cluster_id:
                            hr_df = query_cluster_ubv(alt_cluster_id)
                    if hr_df.empty:        
                        print(f'No UBV data found for {cluster_id}')
                        continue                        
                except Exception as e:
                    print(f'Error fetching {cluster_id}: {e}')
                    continue

                ubv_records = [
                    ClusterUBV(
                        cluster_pk=cluster.pk,
                        b_v=row["b_v"],
                        Mv=row["Mv"]
                    )
                    for _, row in hr_df.iterrows()
                ]

                session.add_all(ubv_records)
                session.commit()
                print(f'Inserted {len(ubv_records)} UBV records for cluster {cluster_id}')
    except Exception as e:
        print(f'Error inserting: {e}')