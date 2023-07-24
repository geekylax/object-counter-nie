import os

from counter.adapters.count_repo import CountMongoDBRepo, CountInMemoryRepo
from counter.adapters.object_detector import TFSObjectDetector, FakeObjectDetector
from counter.domain.actions import CountDetectedObjects
from counter.domain.actions import ListDetectedObjects
from counter.adapters.count_repo import CountInMemoryRepo, CountPostgresRepo
import yaml 

def config(config_path="params.yaml"):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def dev_count_action() -> CountDetectedObjects:
    return CountDetectedObjects(FakeObjectDetector(), CountInMemoryRepo())


def prod_count_action() -> CountDetectedObjects:
    configuration = config()

    tfs_host = configuration['TFS_HOST']

    # tfs_port = os.environ.get('TFS_PORT', 8501)
    tfs_port = configuration['TFS_PORT']
    
    mongo_host = os.environ.get('MONGO_HOST', 'localhost')
    mongo_port = os.environ.get('MONGO_PORT', 27017)
    mongo_db = os.environ.get('MONGO_DB', 'prod_counter')
    countPostgresDB = get_postgres_db()
    # return CountDetectedObjects(TFSObjectDetector(tfs_host, tfs_port, 'rfcn'),
    #                             CountMongoDBRepo(host=mongo_host, port=mongo_port, database=mongo_db))
    return CountDetectedObjects(TFSObjectDetector(tfs_host, tfs_port, 'rfcn'),
                                countPostgresDB)


def get_count_action() -> CountDetectedObjects:
    env = os.environ.get('ENV', 'dev')
    count_action_fn = f"{env}_count_action"
    return globals()[count_action_fn]()


def dev_list_action() -> ListDetectedObjects:
    return ListDetectedObjects(FakeObjectDetector())


def prod_list_action() -> ListDetectedObjects:
    tfs_host = os.environ.get('TFS_HOST', 'localhost')
    tfs_port = os.environ.get('TFS_PORT', 8501)
    countPostgresDB = get_postgres_db()

    return ListDetectedObjects(TFSObjectDetector(tfs_host, tfs_port, 'rfcn'))


def get_list_action() -> ListDetectedObjects:
    env = os.environ.get('ENV', 'dev')
    count_action_fn = f"{env}_list_action"
    return globals()[count_action_fn]()


def get_postgres_db():
    host = os.environ.get('POSTGRES_HOST', 'localhost')
    port = os.environ.get('POSTGRES_PORT', 5432)
    db = os.environ.get('POSTGRES_DB', 'count_db')
    user = os.environ.get('POSTGRES_USER', 'count_user')
    password = os.environ.get('POSTGRES_PASSWORD', 'notsosecretpassword')

    return CountPostgresRepo(host, port, db, user, password)