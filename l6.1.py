class Building:
    def __init__(self, area, cost_per_sqm, num_residents):
        self.area = area
        self.cost_per_sqm = cost_per_sqm
        self.num_residents = num_residents

    def calculate_total_cost(self):

        return self.area * self.cost_per_sqm

    def cost_to_residents_ratio(self):

        if self.num_residents == 0:
            return float('inf')
        return self.calculate_total_cost() / self.num_residents

class VillageHouse(Building):
    def __init__(self, area, cost_per_sqm, num_residents, has_garden):
        super().__init__(area, cost_per_sqm, num_residents)
        self.has_garden = has_garden

    def calculate_total_cost(self):

        base_cost = super().calculate_total_cost()
        if self.has_garden:
            return base_cost * 1.1
        return base_cost

class CityApartment(Building):
    def __init__(self, area, cost_per_sqm, num_residents, floor_count):

        super().__init__(area, cost_per_sqm, num_residents)
        self.floor_count = floor_count

    def cost_to_residents_ratio(self):

        base_ratio = super().cost_to_residents_ratio()
        return base_ratio * (1 + 0.05 * self.floor_count)

if __name__ == "__main__":
    building = Building(200, 1500, 10)
    print("Building Total Cost:", building.calculate_total_cost())
    print("Building Cost-to-Residents Ratio:", building.cost_to_residents_ratio())

    village_house = VillageHouse(150, 1200, 5, has_garden=True)
    print("Village House Total Cost:", village_house.calculate_total_cost())
    print("Village House Cost-to-Residents Ratio:", village_house.cost_to_residents_ratio())

    city_apartment = CityApartment(1000, 2000, 50, floor_count=10)
    print("City Apartment Total Cost:", city_apartment.calculate_total_cost())
    print("City Apartment Cost-to-Residents Ratio:", city_apartment.cost_to_residents_ratio())
