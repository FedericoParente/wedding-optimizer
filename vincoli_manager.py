import streamlit as st

# Funzione per visualizzare i vincoli e gestire le operazioni CRUD
def gestisci_vincoli(vincoli, nomi_ospiti, vincoli_type):
    st.subheader(f"Gestisci vincoli {vincoli_type}")
    
    # Inizializza variabili di sessione per la gestione della modifica
    if f'{vincoli_type}_modifica_idx' not in st.session_state:
        st.session_state[f'{vincoli_type}_modifica_idx'] = None  # Nessun vincolo in modifica

    if f'{vincoli_type}_ospite1' not in st.session_state:
        st.session_state[f'{vincoli_type}_ospite1'] = {}
    
    if f'{vincoli_type}_ospite2' not in st.session_state:
        st.session_state[f'{vincoli_type}_ospite2'] = {}
    
    if f'{vincoli_type}_condizione' not in st.session_state:
        st.session_state[f'{vincoli_type}_condizione'] = {}

    # Visualizza i vincoli
    for idx, vincolo in enumerate(vincoli):
        ospite1, condizione, ospite2 = vincolo

        # Se questo vincolo è in modifica, mostra i widget per modificarlo
        if st.session_state[f'{vincoli_type}_modifica_idx'] == idx:
            # Inizializza i valori modificabili nella sessione, se non già fatto
            if idx not in st.session_state[f'{vincoli_type}_ospite1']:
                st.session_state[f'{vincoli_type}_ospite1'][idx] = ospite1
            if idx not in st.session_state[f'{vincoli_type}_ospite2']:
                st.session_state[f'{vincoli_type}_ospite2'][idx] = ospite2
            if idx not in st.session_state[f'{vincoli_type}_condizione']:
                st.session_state[f'{vincoli_type}_condizione'][idx] = condizione

            # Usa le variabili di sessione per mantenere i valori temporanei
            st.session_state[f'{vincoli_type}_ospite1'][idx] = st.selectbox(
                "Ospite 1", nomi_ospiti, index=nomi_ospiti.index(st.session_state[f'{vincoli_type}_ospite1'][idx]), key=f"{vincoli_type}_osp1_{idx}")
            st.session_state[f'{vincoli_type}_condizione'][idx] = st.radio(
                "Condizione", ["insieme", "separati"], index=["insieme", "separati"].index(st.session_state[f'{vincoli_type}_condizione'][idx]), key=f"{vincoli_type}_cond_{idx}")
            st.session_state[f'{vincoli_type}_ospite2'][idx] = st.selectbox(
                "Ospite 2", nomi_ospiti, index=nomi_ospiti.index(st.session_state[f'{vincoli_type}_ospite2'][idx]), key=f"{vincoli_type}_osp2_{idx}")
            
            # Salva o Annulla la modifica
            if st.button("Salva Modifica", key=f"{vincoli_type}_save_{idx}"):
                vincoli[idx] = (st.session_state[f'{vincoli_type}_ospite1'][idx],
                                st.session_state[f'{vincoli_type}_condizione'][idx],
                                st.session_state[f'{vincoli_type}_ospite2'][idx])
                st.success(f"Vincolo aggiornato: {vincoli[idx]}")
                st.session_state[f'{vincoli_type}_modifica_idx'] = None  # Esci dalla modalità modifica

            if st.button("Annulla", key=f"{vincoli_type}_cancel_{idx}"):
                st.session_state[f'{vincoli_type}_modifica_idx'] = None  # Esci dalla modalità modifica senza salvare

        else:
            col1, col2, col3, col4 = st.columns([3, 3, 2, 2])
            col1.text(f"{ospite1} - {condizione} - {ospite2}")
            if col3.button("Modifica", key=f"{vincoli_type}_mod_{idx}"):
                # Entra nella modalità di modifica
                st.session_state[f'{vincoli_type}_modifica_idx'] = idx

            if col4.button("Elimina", key=f"{vincoli_type}_del_{idx}"):
                vincoli.pop(idx)
                st.warning(f"Vincolo eliminato: {ospite1} {condizione} {ospite2}")
                st.session_state['rerun_flag'] = True  # Forza il ricaricamento dopo l'eliminazione

    # Aggiungi nuovo vincolo
    st.subheader(f"Aggiungi nuovo vincolo {vincoli_type}")
    ospite1 = st.selectbox(f"Ospite 1 ({vincoli_type})", nomi_ospiti, key=f"new_{vincoli_type}_osp1")
    ospite2 = st.selectbox(f"Ospite 2 ({vincoli_type})", nomi_ospiti, key=f"new_{vincoli_type}_osp2")
    condizione = st.radio("Condizione", ["insieme", "separati"], key=f"new_{vincoli_type}_cond")
    if st.button(f"Aggiungi {vincoli_type}"):
        vincoli.append((ospite1, condizione, ospite2))
        st.success(f"Vincolo aggiunto: {ospite1} {condizione} {ospite2}")
