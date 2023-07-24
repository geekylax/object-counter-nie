from typing import List

from pymongo import MongoClient
import psycopg2

from counter.domain.models import ObjectCount
from counter.domain.ports import ObjectCountRepo
from counter.loggers import logging


class CountInMemoryRepo(ObjectCountRepo):

    def __init__(self):
        self.store = dict()

    def read_values(self, object_classes: List[str] = None) -> List[ObjectCount]:
        if object_classes is None:
            return list(self.store.values())

        return [self.store.get(object_class) for object_class in object_classes]

    def update_values(self, new_values: List[ObjectCount]):
        for new_object_count in new_values:
            key = new_object_count.object_class
            try:
                stored_object_count = self.store[key]
                self.store[key] = ObjectCount(key, stored_object_count.count + new_object_count.count)
            except KeyError:
                self.store[key] = ObjectCount(key, new_object_count.count)


class CountMongoDBRepo(ObjectCountRepo):

    def __init__(self, host, port, database):
        self.__host = host
        self.__port = port
        self.__database = database

    def __get_counter_col(self):
        client = MongoClient(self.__host, self.__port)
        db = client[self.__database]
        counter_col = db.counter
        return counter_col

    def read_values(self, object_classes: List[str] = None) -> List[ObjectCount]:
        counter_col = self.__get_counter_col()
        query = {"object_class": {"$in": object_classes}} if object_classes else None
        counters = counter_col.find(query)
        object_counts = []
        for counter in counters:
            object_counts.append(ObjectCount(counter['object_class'], counter['count']))
        return object_counts

    def update_values(self, new_values: List[ObjectCount]):
        counter_col = self.__get_counter_col()
        for value in new_values:
            counter_col.update_one({'object_class': value.object_class}, {'$inc': {'count': value.count}}, upsert=True)

class CountPostgresRepo(ObjectCountRepo):

    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password =  password

    def __connection_add(self):
        client = psycopg2.connect(f"dbname='{self.database}' user='{self.user}' host='{self.host}' port='{self.port}' password='{self.password}'")
        return client

    def read_values(self, object_classes: List[str] = None) -> List[ObjectCount]:
        self.connection = self.__connection_add()

        cur = self.connection.cursor()
        cur.execute("SELECT object_class, observed_count FROM item_count")
        results = cur.fetchall()
        return [ObjectCount(r[0],r[1]) for r in results]

    def update_values(self, new_values: List[ObjectCount]):
        self.connection = self.__connection_add()

        cur = self.connection.cursor()
        for new_value in new_values:
            try:
                cur.execute(f"INSERT INTO item_count (object_class, observed_count)"
                            f" values('{new_value.object_class}', {new_value.count}) "
                            f"ON CONFLICT (object_class) DO "
                            f"UPDATE SET observed_count = item_count.observed_count + excluded.observed_count;")
                self.connection.commit()
                logging.info("Query Commited")
            except Exception as e:
                    logging.error(str(e))


        self.connection.close()