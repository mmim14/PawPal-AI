VALID_TASK_TYPES = {"feeding", "vet", "grooming", "medication", "walks"}


class Task:
    VALID_PRIORITIES = {"low", "medium", "high"}

    def __init__(self, task_type, pet, date, notes="", status="pending", frequency=None, duration=None, priority="medium"):
        """Create a task for a pet with a type, date, and optional notes."""
        if task_type not in VALID_TASK_TYPES:
            raise ValueError(f"task_type must be one of {VALID_TASK_TYPES}")
        if priority not in self.VALID_PRIORITIES:
            raise ValueError(f"priority must be one of {self.VALID_PRIORITIES}")

        self.task_type = task_type
        self.pet = pet
        self.date = date
        self.notes = notes
        self.status = status
        # for recurring tasks like feeding, medication, etc
        self.frequency = frequency
        self.duration = duration
        self.priority = priority

    def mark_complete(self):
        """Mark this task as completed and print a confirmation."""
        self.status = "completed"
        print(f"[{self.task_type.upper()}] {self.pet.name} | {self.date} — marked as completed")

    def get_summary(self):
        """Return a formatted string summarizing all task details."""
        return (
            f"[{self.task_type.upper()}] {self.pet.name} | {self.date}"
            + (f" | {self.notes}" if self.notes else "")
            + (f" | {self.frequency}" if self.frequency else "")
            + (f" | Duration: {self.duration} mins" if self.duration is not None else "")
            + f" | Priority: {self.priority}"
            + f" | Status: {self.status}"
        )


class Pet:
    def __init__(self, name, species, breed, age, gender, medical_notes=""):
        """Initialize a pet with its basic details and an empty task list."""
        self.name = name
        self.species = species
        self.breed = breed
        self.age = float(age)
        self.gender = gender
        self.medical_notes = medical_notes
        self.owner = None
        self.tasks = []  # tasks belonging to this pet

    @property
    def task_count(self):
        """Return the number of tasks assigned to this pet."""
        return len(self.tasks)

    def get_info(self):
        """Return a formatted string of the pet's profile details."""
        owner_name = self.owner.name if self.owner else "Unknown"
        return (
            f"Name: {self.name} | Species: {self.species} | Breed: {self.breed} | "
            f"Age: {self.age} yrs | Gender: {self.gender} | Owner: {owner_name}"
            + (f" | Notes: {self.medical_notes}" if self.medical_notes else "")
        )


class Owner:
    def __init__(self, name):
        """Initialize an owner with a name, empty pet list, and a linked Scheduler."""
        self.name = name
        self.pets = []
        self.scheduler = Scheduler(self)

    def add_pet(self, pet):
        """Add a pet to this owner's list and set the pet's owner back-reference."""
        pet.owner = self
        self.pets.append(pet)

    def get_pets(self):
        """Print profile info for all pets belonging to this owner."""
        for pet in self.pets:
            print(pet.get_info())

    def get_all_tasks(self):
        """Print all tasks across every pet owned by this owner."""
        for pet in self.pets:
            for task in pet.tasks:
                print(task.get_summary())


class Scheduler:
    def __init__(self, owner):
        """Initialize the scheduler linked to a specific owner."""
        self.owner = owner  # queries tasks through owner -> pets -> tasks

    def get_tasks_by_type(self, task_type):
        """Print all tasks of a given type across all of the owner's pets."""
        matches = [
            task
            for pet in self.owner.pets
            for task in pet.tasks
            if task.task_type == task_type
        ]
        for task in matches:
            print(task.get_summary())

    def schedule_feeding_time(self, pet, time, frequency, duration=None, priority="medium"):
        """Create and assign a recurring feeding task to the given pet."""
        if self._has_conflict(pet, time):
            print(f"Conflict: {pet.name} already has a task on {time}")
            return
        task = Task(
            task_type="feeding",
            pet=pet,
            date=time,
            frequency=frequency,
            duration=duration,
            priority=priority,
        )
        pet.tasks.append(task)
        print(f"Scheduled: [FEEDING] {pet.name} | {time} | {frequency}")

    def schedule_vet_appointment(self, pet, date, clinic, frequency=None, duration=None, priority="medium"):
        """Create and assign a vet appointment task, blocking on date conflicts."""
        if self._has_conflict(pet, date):
            print(f"Conflict: {pet.name} already has a task on {date}")
            return
        task = Task(
            task_type="vet",
            pet=pet,
            date=date,
            notes=clinic,
            frequency=frequency,
            duration=duration,
            priority=priority,
        )
        pet.tasks.append(task)
        print(f"Scheduled: [VET] {pet.name} | {date} | {clinic}"
              + (f" | {frequency}" if frequency else ""))

    def schedule_grooming_appointment(self, pet, date, groomer, frequency=None, duration=None, priority="medium"):
        """Create and assign a grooming appointment task, blocking on date conflicts."""
        if self._has_conflict(pet, date):
            print(f"Conflict: {pet.name} already has a task on {date}")
            return
        task = Task(
            task_type="grooming",
            pet=pet,
            date=date,
            notes=groomer,
            frequency=frequency,
            duration=duration,
            priority=priority,
        )
        pet.tasks.append(task)
        print(f"Scheduled: [GROOMING] {pet.name} | {date} | {groomer}"
              + (f" | {frequency}" if frequency else ""))

    def schedule_medication(self, pet, time, frequency, dosage, duration=None, priority="medium"):
        """Create and assign a recurring medication task to the given pet."""
        if self._has_conflict(pet, time):
            print(f"Conflict: {pet.name} already has a task on {time}")
            return
        task = Task(
            task_type="medication",
            pet=pet,
            date=time,
            frequency=frequency,
            notes=dosage,
            duration=duration,
            priority=priority,
        )
        pet.tasks.append(task)
        print(f"Scheduled: [MEDICATION] {pet.name} | {time} | {frequency} | {dosage}")

    def schedule_walk(self, pet, time, duration, frequency, notes="", priority="medium"):
        """Create and assign a recurring walk task to the given pet."""
        if self._has_conflict(pet, time):
            print(f"Conflict: {pet.name} already has a task on {time}")
            return
        task = Task(
            task_type="walks",
            pet=pet,
            date=time,
            notes=notes,
            frequency=frequency,
            duration=duration,
            priority=priority,
        )
        pet.tasks.append(task)
        print(f"Scheduled: [WALKS] {pet.name} | {time} | {frequency} | {duration} mins")

    def _has_conflict(self, pet, date):
        """Return True if the pet already has a task scheduled at the given date."""
        return any(task.date == date for task in pet.tasks)
