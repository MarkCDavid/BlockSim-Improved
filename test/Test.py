import Models

original = Models.Simulation.load_from_file("original.data", lambda: None)
improved = Models.Simulation.load_from_file("improved.data", lambda: None)


print(original.is_similar(improved))