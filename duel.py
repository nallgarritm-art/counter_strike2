import random
from database import update_rating

def fight(p1, p2):
    def power(p):
        return (
            p[2]*0.4 +
            p[3]*0.3 +
            p[4]*0.2 +
            p[5]*0.1 +
            random.randint(-15, 15)
        )

    score1 = power(p1)
    score2 = power(p2)

    if score1 > score2:
        update_rating(p1[0], p1[6] + 15)
        update_rating(p2[0], p2[6] - 10)
        return p1, "AK-47", "Mirage"
    else:
        update_rating(p2[0], p2[6] + 15)
        update_rating(p1[0], p1[6] - 10)
        return p2, "AWP", "Inferno"