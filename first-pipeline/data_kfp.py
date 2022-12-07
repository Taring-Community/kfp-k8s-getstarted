# https://www.kubeflow.org/docs/components/pipelines/v1/sdk/build-pipeline/

import glob
import pandas as pd
import tarfile
import urllib.request
import kfp
import kfp.components as comp

# def download_and_merge_csv( url : str, output_csv: str ):
#     with urllib.request.urlopen( url ) as res:
#         tarfile.open( fileobj=res, mode='r|gz' ).extractall( path='data' )
#     df = pd.concat(
#         [   pd.read_csv( csv_file, header=None )
#             for csv_file in glob.glob( 'data/*.csv' ) 
#         ]
#     )
#     df.to_csv( output_csv, index=False, header=False )

# download_and_merge_csv(
#     url='https://storage.googleapis.com/ml-pipeline-playground/iris-csv-files.tar.gz', 
#     output_csv='merged_data.csv'
# )

#======================= COMPONENTS =======================
# Download and merge CSV files
def merge_csv( 
    file_path: comp.InputPath( 'Tarball' ),
    output_csv: comp.OutputPath( 'CSV' )
):
    import glob
    import pandas as pd
    import tarfile

    tarfile.open( fileobj=file_path, mode='r|gz' ).extractall( path='data' )
    df = pd.concat(
        [   pd.read_csv( csv_file, header=None )
            for csv_file in glob.glob( 'data/*.csv' ) 
        ]
    )
    df.to_csv( output_csv, index=False, header=False )

create_step_merge_csv = comp.create_component_from_func(
    func=merge_csv,
    output_component_file='merge_csv_comp.yaml',
    base_image='python:3.7',
    packages_to_install=[ 'pandas==1.1.4' ]
)