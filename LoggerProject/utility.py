class Utility:
    @staticmethod
    def get_timeformat():
        return '%A %d %B %Y - %I:%M:%S %p'

    @staticmethod
    def mongo_insert(mongo_collection, payload) -> bool:
        # print("MongoColl {}".format(mongo_collection))
        if mongo_collection is not None and payload is not None:
            _id = mongo_collection.insert_one(payload)
            if _id is not None:
                return True
        return False