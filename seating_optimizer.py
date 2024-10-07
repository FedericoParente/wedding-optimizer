from z3 import Int, Optimize, Sum, If, sat

# Funzione generale per gestire l'assegnazione dei posti
def assegna_posti(nomi_ospiti, num_tavoli, max_seats_per_table, vincoli_obbligatori, vincoli_soft):
    ospite_map = {nome: Int(nome) for nome in nomi_ospiti}
    solver = Optimize()

    # Vincolo: Ogni ospite deve essere assegnato a un tavolo tra 0 e num_tavoli-1
    for nome in nomi_ospiti:
        solver.add(ospite_map[nome] >= 0, ospite_map[nome] < num_tavoli)

    # Aggiungi vincoli obbligatori (hard constraints)
    for vincolo in vincoli_obbligatori:
        ospite1, condizione, ospite2 = vincolo
        if condizione == "insieme":
            solver.add(ospite_map[ospite1] == ospite_map[ospite2])
        elif condizione == "separati":
            solver.add(ospite_map[ospite1] != ospite_map[ospite2])

    # Aggiungi vincoli soft (soft constraints)
    for vincolo in vincoli_soft:
        ospite1, condizione, ospite2 = vincolo
        if condizione == "insieme":
            solver.add_soft(ospite_map[ospite1] == ospite_map[ospite2], 1)
        elif condizione == "separati":
            solver.add_soft(ospite_map[ospite1] != ospite_map[ospite2], 1)

    # Vincolo: Ogni tavolo non può avere più del numero massimo di posti
    for t in range(num_tavoli):
        solver.add(Sum([If(ospite_map[nome] == t, 1, 0) for nome in nomi_ospiti]) <= max_seats_per_table)

    if solver.check() == sat:
        model = solver.model()
        seating = {nome: model.evaluate(ospite_map[nome]) for nome in nomi_ospiti}
        return seating
    else:
        return None
