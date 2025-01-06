##############################################
#        Made By - Anthony BUFFET            #
#        Made By - Gregoire MONGREDIEN       #
##############################################


import random
import numpy as np
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

def generate_ternary_table():
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ternary_table = {}
    current_value = [0, 0, 0, 0]  

    for letter in alphabet:
        ternary_table[letter] = current_value[:]
        if letter == "Z":  
            break
        for i in range(len(current_value) - 1, -1, -1):
            current_value[i] += 1
            if current_value[i] > 1:  
                current_value[i] = -1
            else:
                break

    return ternary_table

def mot_to_ternaire(mot, ternary_table):
    return [ternary_table[char] for char in mot if char in ternary_table]

def apply_noise_to_key(key):
    if random.choice([True, False]):
        key = rotate_key(key)
    else:
        key = invert_signs(key)
    return key

def rotate_key(key):
    return key[-1:] + key[:-1]

def invert_signs(key):
    return [-x for x in key]

def generate_cpd(variable_card, evidence_card):
    values = np.random.dirichlet(np.ones(variable_card), size=np.prod(evidence_card)).T
    return values

def apply_bayesian_encoding(key):
    model = BayesianNetwork([
        ("K1", "K2"),
        ("K2", "K3"),
        ("K3", "K4"),
        ("K4", "K5"),
        ("K5", "K6")
    ])
    
    cpd_k1 = TabularCPD(variable="K1", variable_card=2, values=[[0.7], [0.3]])
    cpd_k2 = TabularCPD(variable="K2", variable_card=2, 
                        values=generate_cpd(2, [2]),
                        evidence=["K1"], evidence_card=[2])
    cpd_k3 = TabularCPD(variable="K3", variable_card=2, 
                        values=generate_cpd(2, [2]),
                        evidence=["K2"], evidence_card=[2])
    cpd_k4 = TabularCPD(variable="K4", variable_card=2, 
                        values=generate_cpd(2, [2]),
                        evidence=["K3"], evidence_card=[2])
    cpd_k5 = TabularCPD(variable="K5", variable_card=2, 
                        values=generate_cpd(2, [2]),
                        evidence=["K4"], evidence_card=[2])
    cpd_k6 = TabularCPD(variable="K6", variable_card=2, 
                        values=generate_cpd(2, [2]),
                        evidence=["K5"], evidence_card=[2])

    model.add_cpds(cpd_k1, cpd_k2, cpd_k3, cpd_k4, cpd_k5, cpd_k6)

    assert model.check_model(), "La structure du réseau est invalide"

    inference = VariableElimination(model)

    transformed_key = []
    for i, k in enumerate(key):
        query_result = inference.map_query(["K2", "K3", "K4", "K5", "K6"], evidence={"K1": k % 2})
        new_value = sum(query_result.values()) * k  
        transformed_key.append(int(new_value))
    
    return transformed_key