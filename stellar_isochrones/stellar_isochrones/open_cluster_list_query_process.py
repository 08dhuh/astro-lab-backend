# class StarCluster(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str
#     star_count: int
#     reddening: Optional[float] = None #E(B-V)
#     fe_h: Optional[float] = None #[Fe/H]
#     distance_pc: Optional[float] = None #distance in parsecs
#     log_age: Optional[float] = None #log age in years

# class ClusterUBV(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     cluster_id: int = Field(foreign_key="starcluster.id")
#     v_mag: float #Apparent V-band magnitude
#     b_v: float  #B-V colour index

cluster_df_columns = ['id', 'name', 'star_count']