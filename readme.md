# Aircraft Runway Scheduling Problem - Genetic Algorithm Solution

This project solves the Aircraft Runway Scheduling Problem using a Genetic Algorithm in Python. The objective is to schedule landings in an optimal sequence to minimize delays, taking into account constraints such as separation time between aircraft and runway availability.

## Features

-   Solves runway scheduling using a Genetic Algorithm.
-   Optimizes landing times to reduce delays.
-   Handles constraints such as aircraft separation time.
-   Configurable population size, mutation rate, and generations.

## Technology Stack

-   Python
-   Genetic Algorithm implementation

## How It Works

-   **Initialization**: A population of potential landing schedules is randomly generated.
-   **Fitness Evaluation**: Each schedule is evaluated based on the total delay and separation time violations.
-   **Selection**: The best-performing schedules are selected for the next generation.
-   **Crossover**: Selected schedules are combined to create new offspring.
-   **Mutation**: Random changes are introduced to maintain diversity in the population.
-   **Termination**: The process repeats for a defined number of generations, or until an optimal solution is found.
