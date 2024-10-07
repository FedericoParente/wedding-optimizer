import streamlit as st
from seating_optimizer import assegna_posti
from vincoli_manager import gestisci_vincoli

# Configurazione della GUI di Streamlit
st.title("Wedding Optimizer")
# Aggiungi il nome sotto il titolo in formato piccolo
st.markdown('<p style="font-size:12px; color:gray;">by Federico</p>', unsafe_allow_html=True)


# Sezione per inserire il numero di tavoli e il numero massimo di posti per tavolo
num_tavoli = st.number_input("Numero di tavoli", min_value=1, value=3, step=1)
max_seats_per_table = st.number_input("Numero massimo di posti per tavolo", min_value=1, value=2, step=1)

# Sezione per inserire i nomi degli ospiti
nomi_ospiti = st.text_area("Inserisci i nomi degli ospiti, separati da virgola", "Alice, Bob, Charlie, Daisy, Eve, Frank")
nomi_ospiti = [nome.strip() for nome in nomi_ospiti.split(",")]

# Inizializzazione delle liste di vincoli nella sessione per persistenza
if 'vincoli_obbligatori' not in st.session_state:
    st.session_state.vincoli_obbligatori = []

if 'vincoli_soft' not in st.session_state:
    st.session_state.vincoli_soft = []

# Gestisci vincoli obbligatori (hard constraints)
gestisci_vincoli(st.session_state.vincoli_obbligatori, nomi_ospiti, "obbligatori")

# Gestisci vincoli soft (soft constraints)
gestisci_vincoli(st.session_state.vincoli_soft, nomi_ospiti, "soft")

# Esegui l'ottimizzazione quando l'utente preme il bottone
if st.button("Esegui ottimizzazione"):
    seating = assegna_posti(nomi_ospiti, num_tavoli, max_seats_per_table, st.session_state.vincoli_obbligatori, st.session_state.vincoli_soft)
    if seating:
        st.success("Assegnazione completata!")
        
        # Crea una struttura per visualizzare i tavoli
        tavoli = {t: [] for t in range(num_tavoli)}  # Dizionario per memorizzare ospiti per tavolo

        # Assegna gli ospiti ai tavoli
        for nome, tavolo in seating.items():
            tavoli[tavolo.as_long()].append(nome)
        
        # Visualizza i tavoli e gli ospiti
        for tavolo_num, ospiti in tavoli.items():
            st.subheader(f"Tavolo {tavolo_num + 1}")  # Numero del tavolo
            if ospiti:
                st.write(", ".join(ospiti))  # Ospiti assegnati al tavolo
            else:
                st.write("Tavolo vuoto")  # Se il tavolo non ha ospiti
    else:
        st.error("Non è possibile trovare una soluzione con i vincoli forniti.")
