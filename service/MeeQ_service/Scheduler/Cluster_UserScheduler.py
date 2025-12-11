from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import Depends
from datetime import datetime

from repository.MeeQ_repository.Cluster_UserPageRepository import ClusterUserPageRepository



class ClusterUserScheduler:
    scheduler = BackgroundScheduler()
    clusterUserPageRepository = ClusterUserPageRepository()

    @staticmethod
    def check_date_and_time(date:datetime) -> bool:
        now = datetime.now()
        if now > date:
            return True # Current time is greater than the timestamp 
        else:
            return False # Current time is lesser than the timestamp 


    @staticmethod
    def my_task():
        cursor = ClusterUserScheduler.clusterUserPageRepository._get_all_Conference_room()
        all_docs = list(cursor) 

        for doc in all_docs:
            for building in doc['buildings']:
                for timeslots in building['time_slots']:
                    state = ClusterUserScheduler.check_date_and_time(timeslots['end_time'])
                    if state:
                        cluster_id = doc['cluster_id']
                        time_slot_id = timeslots['id']
                        result = ClusterUserScheduler.clusterUserPageRepository.delete_time_slot(cluster_id,time_slot_id)
      
        cursor.close()
       
    scheduler.add_job(my_task, 'interval', seconds=10)


    