from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass


    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def MineMax():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select min(s.Lat) as latMin, max(s.Lat ) as latMax , min(s.Lng) as lonMin, max(s.Lng ) as lonMax
                        from state s 
            """
            cursor.execute(query)

            for row in cursor:
                result.append((row["latMin"], row["latMax"], row["lonMin"], row["lonMax"]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getShapes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct s.shape 
                        from sighting s 
                        where s.shape !=""
                        order by s.shape 
                """
            cursor.execute(query)

            for row in cursor:
                result.append(row["shape"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getNodes(lat, lon, shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select  s.* 
                    from state s, sighting s1
                    where s.id = s1.state 
                    and s.Lat  > %s
                    and s.Lng   > %s
                    and s1.shape = %s
                    group by s1.state  , s1.shape 
                    having count(*)>=1
                    """
            cursor.execute(query,(lat,lon,shape))

            for row in cursor:
                result.append(State(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAvvistamenti(lat, lon, shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """
                    select  s.id, s.Neighbors as vicini, s1.duration 
                    from state s, sighting s1
                    where s.id = s1.state 
                    and s.Lat  >%s
                    and s.Lng   > %s
                    and s1.shape =%s
                    """
            cursor.execute(query,(lat, lon, shape))

            for row in cursor:
                result.append((row["id"], row["vicini"], row["duration"]))
            cursor.close()
            cnx.close()
        return result

