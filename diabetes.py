import numpy as np

transition_matrix = [
    [0.70, 0.20, 0.05, 0.05],   # matrix that calculates the probability of shifting from one state to another
    [0.10, 0.60, 0.25, 0.05],
    [0.05, 0.15, 0.70, 0.10],
    [0.00, 0.00, 0.00, 1.00]  # not possible to cure from diabetes
]

states = ["Low Risk", "Moderate Risk", "High Risk", "Diabetes"]  # states
mutation_probability = 0.02


def get_yes_no_input(prompt): #prompt - string type
    while True:
        response = input(prompt).strip().lower()
        if response in ["yes", "no"]:
            return response
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


def get_age_input(prompt):
    while True:
        try:
            age = int(input(prompt).strip())
            if 0 < age <= 130:
                return age
            else:
                print("Invalid input. Please enter an age between 1 and 130.")
        except ValueError:
            print("Invalid input. Please enter a valid number for age.")


def calculate_initial_state():
    print("Welcome to the Diabetes Risk Prediction Program!")

    parent1 = get_yes_no_input("Did your first parent (mother/father) have diabetes? (yes/no): ")  # passing the message to prompt argument
    parent2 = get_yes_no_input("Did your second parent (mother/father) have diabetes? (yes/no): ")

    age = get_age_input("How old are you? (in years): ")
    weight_status = get_yes_no_input("Do you consider yourself overweight? (yes/no): ")
    physical_activity = get_yes_no_input("Do you engage in physical activities at least 3 times a week? (yes/no): ")

    risk_score = 0  # initial risk score is 0. Maximum - 0

    if parent1 == "yes" and parent2 == "yes":
        risk_score += 3
    elif parent1 == "yes" or parent2 == "yes":
        risk_score += 2
    else:
        risk_score += 1

    if age > 45:
        risk_score += 2
    elif age > 30:
        risk_score += 1

    if weight_status == "yes":
        risk_score += 2

    if physical_activity == "no":
        risk_score += 2

    if risk_score >= 7:
        return "High Risk"
    elif 4 <= risk_score < 7:
        return "Moderate Risk"
    else:
        return "Low Risk"


def apply_mutation(current_state):
    mutation_effect = mutation_probability / len(states) #calculates the distribution of probability accross all states
    mutated_state = np.full(len(states), mutation_effect)   #makes numpy array with all probabilities
    non_mutation_prob = 1 - mutation_probability # calculates the probability og no mutation
    return non_mutation_prob * current_state + mutated_state

    # calculates stability(no change in state) and adds uniformly distributed prob to each state to update the chance of diabetes

def predict_diabetes_risk(initial_state, steps):  # steps - number of years
    state_index = states.index(initial_state)
    current_state = np.zeros(len(states))  # creates an array with 0 and length-equal to the number of states
    current_state[state_index] = 1 # updates index of state to 1, all other 0

    for _ in range(steps):
        current_state = np.dot(current_state, transition_matrix) # updates the current probability after n-years        current_state = apply_mutation(current_state)
        current_state = apply_mutation(current_state) # considers probability of mutation
    return dict(zip(states, current_state))  # connects states with probabilities and make dictionary


initial_state = calculate_initial_state()
steps = 5
predicted_risk = predict_diabetes_risk(initial_state, steps)

print(f"\nPredicted risk distribution after {steps} steps starting from '{initial_state}':")
for state, probability in predicted_risk.items():
    print(f"{state}: {probability:.2%}")