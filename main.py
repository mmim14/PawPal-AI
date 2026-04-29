from datetime import date
from pawpal_system import Pet, Owner, Task

owner = Owner("Mimi")

minmin = Pet(name="Minmin", species="Cat", breed="American Shorthair", age=5, gender="Female")
pichu  = Pet(name="Pichu",  species="Cat", breed="American Shorthair", age=1.5, gender="Male")
mochi  = Pet(name="Mochi",  species="Cat", breed="Maine Coon", age=.5, gender="Male")

owner.add_pet(minmin)
owner.add_pet(pichu)
owner.add_pet(mochi)

# Task 1: Vet appointment for Minmin on 4/15/2026 at 11 AM
owner.scheduler.schedule_vet_appointment(minmin, "2026-04-15 11:00 AM", "City Animal Clinic")

# Task 2: Feeding for Pichu every 4 hours
owner.scheduler.schedule_feeding_time(pichu, "2026-04-01", "every 4 hours")

# Task 3: Grooming appointment for Mochi on 4/21/2026 at 3 PM
owner.scheduler.schedule_grooming_appointment(mochi, "2026-04-21 3:00 PM", "Fluffy Paws Grooming")

# Print today's schedule
today = str(date.today())
print(f"\n--- Today's Schedule ({today}) ---")
for pet in owner.pets:
    for task in pet.tasks:
        if task.date.startswith(today):
            print(task.get_summary())
