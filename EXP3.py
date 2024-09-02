class CandidateEliminationLearner:
    def __init__(self, attributes):
        # Initialize the specific and general boundaries
        self.attributes = attributes
        self.G = [self.general_hypothesis()]
        self.S = [self.specific_hypothesis()]

    def general_hypothesis(self):
        # The most general hypothesis, assumes any input is possible
        return {attr: 'any' for attr in self.attributes}

    def specific_hypothesis(self):
        # The most specific hypothesis, assumes no input is possible
        return {attr: 'none' for attr in self.attributes}

    def is_more_general(self, h1, h2):
        # Check if hypothesis h1 is more general than hypothesis h2
        for attr in self.attributes:
            if h1[attr] != 'any' and (h2[attr] == 'any' or h1[attr] != h2[attr]):
                return False
        return True

    def generalize(self, hypothesis, example):
        # Create the minimal generalizations of the hypothesis to cover the positive example
        new_hypothesis = hypothesis.copy()
        for attr in self.attributes:
            if example[attr] != hypothesis[attr]:
                new_hypothesis[attr] = 'any'
        return new_hypothesis

    def specialize(self, hypothesis, example):
        # Create the minimal specializations of the hypothesis to exclude the negative example
        new_hypotheses = []
        for attr in self.attributes:
            if hypothesis[attr] == 'any':
                for value in example.values():
                    if value != example[attr]:
                        new_hypothesis = hypothesis.copy()
                        new_hypothesis[attr] = value
                        new_hypotheses.append(new_hypothesis)
        return new_hypotheses

    def update_boundaries(self, example, is_positive):
        if is_positive:
            # Remove inconsistent hypotheses from G
            self.G = [g for g in self.G if not self.is_more_general(g, example)]
            # Generalize S
            new_S = []
            for s in self.S:
                if not self.is_more_general(s, example):
                    new_hypothesis = self.generalize(s, example)
                    if all(self.is_more_general(g, new_hypothesis) for g in self.G):
                        new_S.append(new_hypothesis)
            self.S = new_S
            # Remove non-maximal hypotheses from S
            self.S = [s for s in self.S if all(not self.is_more_general(other_s, s) for other_s in self.S)]
        else:
            # Remove inconsistent hypotheses from S
            self.S = [s for s in self.S if not self.is_more_general(example, s)]
            # Specialize G
            new_G = []
            for g in self.G:
                if not self.is_more_general(example, g):
                    new_hypotheses = self.specialize(g, example)
                    for new_hypothesis in new_hypotheses:
                        if all(not self.is_more_general(new_hypothesis, s) for s in self.S):
                            new_G.append(new_hypothesis)
            self.G = new_G
            # Remove non-minimal hypotheses from G
            self.G = [g for g in self.G if all(not self.is_more_general(g, other_g) for other_g in self.G)]

    def learn(self, examples):
        for example, is_positive in examples:
            self.update_boundaries(example, is_positive)
        return self.G, self.S

# Example usage
if __name__ == "__main__":
    attributes = ['color', 'size', 'shape']
    examples = [
        ({'color': 'red', 'size': 'small', 'shape': 'circle'}, True),
        ({'color': 'blue', 'size': 'large', 'shape': 'square'}, False),
        # Add more examples here
    ]
    
    learner = CandidateEliminationLearner(attributes)
    G, S = learner.learn(examples)
    
    print("General Hypotheses:", G)
    print("Specific Hypotheses:", S)
