from database.distributore_DAO import DistributoreDAO
from model.prezzo_DTO import Prezzo

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._distributori = None
        self.load_distributori()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_distributori(self):
        """ Carica tutti i distributori e li setta nella variabile self._distributori """
        self._distributori = DistributoreDAO.get_distributori()

    def get_prezzo_medio(self, mese:int):
        """
        Calcola, per ogni distributore, il prezzo medio al litro per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome del distributore, media), es. (Distributore A, 1.789)
        """
        # TODO

        prezzi_al_mese = [] # lista con risultato per ogni distributore

        for distributore in self._distributori:
            somma_prezzi_al_mese = 0
            totali = 0
            for prezzo in distributore.get_prezzi(): # distributore.get_prezzi() interroga il DB (tramite il DAO) e
                # restituisce tutti i prezzi dell'anno di QUEL distributore, come oggetti Prezzo
                if prezzo.data.month == mese:
                    somma_prezzi_al_mese += prezzo.prezzo_litro
                    totali += 1
            media = somma_prezzi_al_mese / totali
            tupla = (distributore.nome, media)
            prezzi_al_mese.append(tupla)
        return prezzi_al_mese

    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di rifornimenti nei primi 7 giorni
        :return: sequenza di nomi distributore ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        prezzi_settimana = self.__get_prezzi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, prezzi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {distributore.id: distributore.nome for distributore in self._distributori}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, round(self.__costo_ottimo, 2)

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_distributore, costo_corrente, prezzi_settimana):
        """ Implementa la ricorsione """
        # TODO

        if len(sequenza_parziale) == 7:
            pass
        else:
            # Provo, per questo giorno, ogni distributore possibile (le chiavi sono gli id)
            for id_distributore in prezzi_settimana:

                # Le liste partono da 0, i giorni da 1: il giorno 1 è la posizione 0.
                # Costo del giorno = prezzo al litro * 100 litri
                costo_giorno = prezzi_settimana[id_distributore][giorno - 1] * 100

                # +5€ solo se cambio distributore. Il primo giorno ultimo_distributore
                # è None: non c'è uno spostamento, quindi niente costo fisso.
                if ultimo_distributore is not None and ultimo_distributore != id_distributore:
                    costo_giorno += 5

                # ora scelgo questo distributore, scendo al giorno successivo, poi torno indietro

    def __get_prezzi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i prezzi dei primi 7 giorni del mese selezionato per ciascun distributore.
        :return: un dizionario: {id_distributore: [prezzo_giorno1, ..., prezzo_giorno7]}
        """
        # TODO
        prezzi_settimana = {}

        for distributore in self._distributori:
            prezzo_al_giorno = []
            for prezzo in sorted(distributore.get_prezzi(), key=lambda x:x.data):
                # distributore.get_prezzi() restituisce tutti i prezzi dell'anno
                # (oggetti Prezzo) di QUEL distributore, è una lista ordinata cronologicamente tramite sorted()
                if prezzo.data.month == mese and prezzo.data.day <= 7: # tengo solo i prezzi del mese scelto e
                    # dei giorni dall'1 al 7 compresi
                    prezzo_al_giorno.append(prezzo.prezzo_litro) #append modifica la lista subito e restituisce None
            prezzi_settimana[distributore.id] = prezzo_al_giorno
            # salvo la lista nel dizionario con l'id del distributore come chiave
            # viene eseguita una volta per distributore, a lista completa
        return prezzi_settimana
