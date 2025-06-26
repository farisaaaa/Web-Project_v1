import pandas as pd
import random
import pickle
from geopy.distance import geodesic
import os

# Load dataset
df = pd.read_csv("Data1st.csv")

# Fungsi untuk ngambil data branch per kendaraan
def prepare_branch_data(df, vehicle_type):
    df_filtered = df[df["Vehicle_Type_Assigned"] == vehicle_type]
    df_branch = df_filtered[['Branch_Start', 'Start_Latitude', 'Start_Longitude']].drop_duplicates().reset_index(drop=True)
    return df_branch

# Fungsi GA
def genetic_algorithm_routing(df_branch, pop_size=50, generations=300, mutation_rate=0.1):
    branches = df_branch['Branch_Start'].tolist()
    coords = list(zip(df_branch['Start_Latitude'], df_branch['Start_Longitude']))

    # Buat distance matrixnya
    distance_matrix = {
        (branches[i], branches[j]): geodesic(coords[i], coords[j]).km
        for i in range(len(branches))
        for j in range(len(branches)) if i != j
    }

    def calculate_distance(route):
        return sum(
            distance_matrix[(route[i], route[i+1])]
            for i in range(len(route) - 1)
        ) + distance_matrix[(route[-1], route[0])]

    # Inisialisasi populasi
    population = [random.sample(branches, len(branches)) for _ in range(pop_size)]

    for _ in range(generations):
        population = sorted(population, key=calculate_distance)
        new_population = population[:10]  # elitism

        while len(new_population) < pop_size:
            p1, p2 = random.sample(population[:30], 2)
            start, end = sorted(random.sample(range(len(branches)), 2))
            child = [None] * len(branches)
            child[start:end] = p1[start:end]

            pointer = 0
            for gene in p2:
                if gene not in child:
                    while child[pointer] is not None:
                        pointer += 1
                    child[pointer] = gene

            if random.random() < mutation_rate:
                a, b = random.sample(range(len(branches)), 2)
                child[a], child[b] = child[b], child[a]

            new_population.append(child)
        
        population = new_population

    best_route = population[0]
    best_distance = calculate_distance(best_route)

    return {
        "route": best_route,
        "distance": round(best_distance, 2),
        "branches": df_branch
    }

# Eksekusi dan simpan model tiap kendaraan
vehicle_types = df["Vehicle_Type_Assigned"].dropna().unique()
os.makedirs("model_ga", exist_ok=True)

for vt in vehicle_types:
    df_branch = prepare_branch_data(df, vt)
    if len(df_branch) > 1:
        result = genetic_algorithm_routing(df_branch)
        
        # Simpan ke .pkl
        filename = f"model_ga/GA_model_{vt.replace(' ', '_').lower()}.pkl"
        with open(filename, "wb") as f:
            pickle.dump(result, f)

        print(f"✅ Model untuk '{vt}' disimpan ke: {filename}")
        print("   Rute:", " -> ".join(result['route']))
        print("   Jarak total:", result['distance'], "km")
