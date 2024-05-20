class Polynomial:
    def __init__(self, *coefficients):
        if isinstance(coefficients[0], dict):
            self.coefficients = coefficients[0]
        elif isinstance(coefficients[0], list):
            self.coefficients = {i: coefficients[0][i] for i in range(len(coefficients[0]))}
        else:
            self.coefficients = {i: coefficients[i] for i in range(len(coefficients))}

    def __repr__(self):
        res = str(list(self.coefficients.values()))
        return f'Polynomial {res}'

    def __str__(self):
        result = ""
        for degree in sorted(self.coefficients.keys(), reverse=True):
            coeff = self.coefficients[degree]
            if coeff == 0:
                result += "0"
                return result
            if degree == 0:
                result += f" + {coeff}" if coeff > 0 else f" - {-coeff}"
            elif degree == 1:
                result += f" + {coeff}x" if coeff > 0 else f" - {-coeff}x"
            else:
                result += f" + {coeff}x^{degree}" if coeff > 0 else f" - {-coeff}x^{degree}"
        return result.lstrip(' +')

    def __eq__(self, other):
        if not isinstance(other, Polynomial):
            return False
        return self.coefficients == other.coefficients

    def __add__(self, other):
        if not isinstance(other, Polynomial):
            other = Polynomial(other)
        result_poly = self.coefficients.copy()
        for degree, coeff in other.coefficients.items():
            if degree in result_poly:
                result_poly[degree] += coeff
            else:
                result_poly[degree] = coeff
        return Polynomial(result_poly)

    def __radd__(self, other):
        return self.__add__(other)

    def __neg__(self):
        negated_coeffs = {degree: -coeff for degree, coeff in self.coefficients.items()}
        return Polynomial(negated_coeffs)

    def __sub__(self, other):
        return self.__add__(-other)

    def __rsub__(self, other):
        return (-self).__add__(other)

    def __call__(self, x):
        result = 0
        for power, coeff in self.coefficients.items():
            result += coeff * (x ** power)
        return result

    def degree(self):
        return max(self.coefficients.keys(), default=-1)

    def der(self, d=1):
        res = self.coefficients.copy()
        while d > 0:
            temp = {}
            for degree, coeff in res.items():
                if degree > 0:
                    temp[degree - 1] = degree * coeff
            res = temp
            d -= 1
        return Polynomial(res)

    def __mul__(self, other):
        if not isinstance(other, Polynomial):
            other = Polynomial(other)
        result = {}
        for deg1, coeff1 in self.coefficients.items():
            for deg2, coeff2 in other.coefficients.items():
                new_deg = deg1 + deg2
                new_coeff = coeff1 * coeff2
                if new_deg in result:
                    result[new_deg] += new_coeff
                else:
                    result[new_deg] = new_coeff
        return Polynomial(result)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __iter__(self):
        return iter(self.coefficients.items())

    def __next__(self):
        return next(iter(self.coefficients.items()))