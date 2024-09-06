import random
import time
import sys

# Airplane Class
class Airplane:
    # initialize airplane
    def __init__(self, properties, separations, name):
      self.arrival_time = int(properties[0])
      self.earliest_time = int(properties[1])
      self.target_time = int(properties[2])
      self.latest_time = int(properties[3])
      self.early_penalty = float(properties[4])
      self.late_penalty = float(properties[5])
      self.separations = {index: value for index, value in enumerate(separations)}
      self.name = name

    def __str__(self):
      res = f"========\nAirplane {self.name}\nArrival Time: {self.arrival_time}\nEarliest Time: {self.earliest_time}\nTarget Time: {self.target_time}\nLatest Time: {self.latest_time}\nEarly Penalty:{self.early_penalty}\nLate Penalty:{self.late_penalty}\n"

      res += " ".join([str(x) for x in self.separations]) 

      return res
    
    def encoder(self, time):
      return bin(time - self.earliest_time)[2:]
    
    def decoder(self, gene):
      return int(gene,2) + self.earliest_time

class GeneticAlgorithm:
  def __init__(self, data):
    # initialize environment for genetic algorithm
    self.data = data 


  def create_population(self, population_count):
    # create population
    population = []

    counter = 0

    # create individuals
    while len(population) < population_count:
        # checker if we can create a single individual from the set
        if counter > 10000 and not len(population):
           print("Failed to create a single individual after 10000 tries!")
           sys.exit()

        individual = []

        # generate individual
        for key, plane in self.data.items():
           time = plane.target_time if plane.earliest_time == plane.latest_time else random.randint(plane.earliest_time, plane.latest_time)
           individual.append([key, time])

        # sort the order of the aircrafts based on their landing times
        individual = self.adjust_individual(sorted(individual, key= lambda x: x[1]))

        # add individual
        if individual:
            population.append(individual)
        
        # increment counter
        counter += 1

    # return created population
    return population
  
  def valid_individual(self, schedule):
    prevPlane,prevTime = schedule[0]

    for i in range(1, len(schedule)):
      plane, time = schedule[i]
      proper_time = prevTime + self.data[prevPlane].separations[plane]

      if time < proper_time:
        return False


    return True
  
  def adjust_individual(self, schedule):
    # use this function to adjust the landing time of every individual
    prevPlane, prevTime = schedule[0]


    individual = {prevPlane: self.data[prevPlane].encoder(prevTime)}

    for i in range(1, len(schedule)):
      plane, time = schedule[i]
      proper_time = prevTime + self.data[prevPlane].separations[plane]

      time = time if time >= proper_time else proper_time

      # Check if we have a valid time
      if time > self.data[plane].latest_time:
         return None

      # Add plane
      individual[plane] = self.data[plane].encoder(time)
      prevPlane = plane
      prevTime = time

    return individual

  def crossover(self, parent1, parent2):
    # create copies of the parent
    offspring1 = dict(parent1)
    offspring2 = dict(parent2)

    # number of planes to crossover
    num_planes = random.randint(1, len(parent1) - 1)

    # crossover
    for _ in range(num_planes):
      # choose a random plane to do crossover
      plane = random.randint(0, len(parent1) - 1)

      # find length of string of plane
      length = len(parent1[plane])

      # Select a random crossover point
      crossover_point = random.randint(0, length - 1)
      
      # Perform crossover
      offspring1[plane] = parent1[plane][:crossover_point] + parent2[plane][crossover_point:]
      offspring2[plane] = parent2[plane][:crossover_point] + parent1[plane][crossover_point:]
    
    # return offspring
    return offspring1, offspring2
  
  def mutate(self, individual):
    plane = random.randint(0, len(individual) - 1)

    # generate two random crossover points
    point = random.randint(0, len(individual[plane]) - 1)

    # turn on point
    binary_string = list(individual[plane])
    binary_string[point] = '1'

    individual[plane] = "".join(binary_string)

  
  # breed the population
  def breed_population(self, population, selection_probability):
    new_population = []

    # add elites
    for _ in range(10):
      new_population.append(random.choices(population, weights=selection_probability)[0])

    while len(new_population) < len(population):
      # choose parents
      parent1 = random.choices(population, weights=selection_probability)[0]
      parent2 = random.choices(population, weights=selection_probability)[0]

      # generate offsprings
      offspring1, offspring2 = self.crossover(parent1, parent2)

      # do mutation
      if random.randint(1, 10) == 1:
          self.mutate(random.choice([offspring1, offspring2]))

      individuals = sorted([parent1, parent2, offspring1, offspring2], key= lambda x: self.compute_fitness(x))

      # add offspring
      new_population.append(individuals[0])
      new_population.append(individuals[1])

    return new_population
  
  def compute_fitness(self, individual):
    # get the permutation
    permutation = [x for x in individual.keys()]

    # fitness function
    penalty = 0
    index = 0

    prev_time = 0
    # iterate every time slots of individual
    for name, value in individual.items():
      plane = self.data[name]
      current_time = plane.decoder(value)

      if index > 0:
        prev_plane = self.data[permutation[index - 1]]

        # check if separation was enforced
        if current_time < prev_time + prev_plane.separations[plane.name]:
           return float("inf")

      if current_time < plane.target_time:
        penalty += (plane.target_time - current_time) * plane.early_penalty
      else:
        penalty += (current_time - plane.target_time) * plane.late_penalty   
     

      prev_time = current_time
      index += 1

    return penalty

  def calculate_probability(self, population):
    fitness = [self.compute_fitness(individual) for individual in population]
    
    sum = 0

        # compute for total sum of score
    for score in fitness:
        if score == float("inf") or score < 0:
            continue
        sum += score

    selection_probability = []

    for score in fitness:
        if score == float("inf") or score < 0:
            selection_probability.append(0)
            continue

        selection_probability.append(sum / score)

    return selection_probability

  def has_converged(self, population):
     # check if all the solutions already have equal data
     return all(individual == population[0] for individual in population)

  def simulate(self, generations, population):
    start_time = time.time()
    population = self.create_population(population)
    probability = self.calculate_probability(population)

    generation = 0
    best_individual = population[probability.index(max(probability))]

    while not self.has_converged(population) and generation < generations:
      population = self.breed_population(population, probability)
      probability = self.calculate_probability(population)
  
      # update best individual
      best_individual = population[probability.index(max(probability))]

      # update current generation
      generation += 1
    # print best winner
    print(f'======== FINAL WINNER AFTER {generation} GENERATIONS ========\nHere\'s the best schedule based on the Genetic Algorithm Implementation:')
    print("Airline Schedule:")

    for key, val in best_individual.items():
      val = str(self.data[key].decoder(val))
      suffix = 'th'

      if val[len(val) - 1] == '1':
        suffix = 'st'
      elif val[len(val) - 1] == '2':
        suffix = 'nd'
      elif val[len(val) - 1] == '3':
        suffix = 'rd'

      print(f"Airplane {key} will arrive on the {val}{suffix} of the time.")
    
    print(f"DNA OF SOLUTION:\n{''.join(best_individual.values())}")      
    print(f"PENALTY INCURRED: {self.compute_fitness(best_individual)}\n")
    end_time = time.time()

    print(f"Execution Time: {end_time - start_time} seconds")
    
  

class Program:
  def start(self, filename, generations, population):
    data = self.read_file(filename)

    # initiaize instance of genetic algorithm
    genetic_algorithm = GeneticAlgorithm(data)
    
    # start simulation
    genetic_algorithm.simulate(generations, population)

  def read_file(self, filename):
    # use this function to read input files
    data = {}

    with open(filename, 'r') as file:
      file_paths = file.readlines()
      file_paths = [path.strip() for path in file_paths]
    
      count = 0
      for i in range(1, len(file_paths), 2):
        properties, separations = file_paths[i], file_paths[i+1]
        new_properties = [x for x in properties.split(" ")]
        new_separations = [int(x) for x in separations.split(" ")]
        plane = Airplane(new_properties, new_separations, count)
        data[count] = plane

        count += 1
    
    return data


