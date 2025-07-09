from database.DB_connect import DBConnect
from model.classification import Classification
from model.gene import Gene
from model.interaction import Interaction


class DAO():

    @staticmethod
    def get_all_genes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                        FROM genes"""
            cursor.execute(query)

            for row in cursor:
                result.append(Gene(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_interactions():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                           FROM interactions"""
            cursor.execute(query)

            for row in cursor:
                result.append(Interaction(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_classifications(location):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT c.GeneID, c.Localization, g.Chromosome 
                        FROM classification c, genes g 
                        WHERE c.Localization = %s
                            AND c.GeneID = g.GeneID 
                            AND g.Essential IS NOT NULL 
                        """
            cursor.execute(query, (location, ))

            for row in cursor:
                result.append(Classification(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_localizations():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                        SELECT DISTINCT c.Localization 
                        FROM classification c 
                        ORDER BY c.Localization DESC
                        """

            cursor.execute(query, )
            result = []
            for row in cursor.fetchall():
                result.append(row['Localization'])
            return result
        finally:
            cursor.close()
            conn.close()


