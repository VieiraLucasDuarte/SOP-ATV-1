from CPU import CPU

def initialize_cpus(count):
    return [CPU(f"CPU-{i}") for i in range(count)]

def initialize_tasks(tasks):
    for task in tasks:
        task["remainingDuration"] = task["totalDuration"]
    return sort_tasks_by_quantum_desc(tasks)

def sort_tasks_by_quantum_desc(tasks):
    for i in range(len(tasks)):
        for j in range(i + 1, len(tasks)):
            if tasks[i]["quantum"] < tasks[j]["quantum"]:
                tasks[i], tasks[j] = tasks[j], tasks[i]
    return tasks

def create_cpu_history(cpus):
    history = {}
    for cpu in cpus:
        history[cpu.name] = []
    return history

def run_scheduler(tasks, cpus, cpu_history):
    completed_tasks = []
    CYCLE_DURATION = 5  # Cada ciclo é de 5 segundos

    while len(completed_tasks) < len(tasks):
        available_cpus = cpus[:]
        execution_queue = []

        for task in tasks:
            if task["id"] in completed_tasks:
                continue
            if len(available_cpus) >= task["requiredCpus"]:
                allocated_cpus = []
                for _ in range(task["requiredCpus"]):
                    allocated_cpus.append(available_cpus.pop(0))
                execution_queue.append((task, allocated_cpus))

        for task, allocated_cpus in execution_queue:
            # Calcular quantos ciclos de 5 segundos esta tarefa irá ocupar
            cycles_needed = task["quantum"] // CYCLE_DURATION
            if task["quantum"] % CYCLE_DURATION > 0:
                cycles_needed += 1
            
            # Executar por no máximo o tempo restante
            execution_time = min(task["quantum"], task["remainingDuration"])
            task["remainingDuration"] -= execution_time
            
            # Adicionar entradas para cada ciclo de 5 segundos
            for i in range(cycles_needed):
                cycle_time = min(CYCLE_DURATION, execution_time - (i * CYCLE_DURATION))
                if cycle_time <= 0:
                    break
                    
                for cpu in allocated_cpus:
                    cpu_history[cpu.name].append(f"{task['id']}({cycle_time})")
            
            if task["remainingDuration"] <= 0:
                completed_tasks.append(task["id"])

def fill_cpu_history(cpu_history):
    max_length = 0
    for history in cpu_history.values():
        if len(history) > max_length:
            max_length = len(history)

    for history in cpu_history.values():
        while len(history) < max_length:
            history.append(".")
    return max_length

def print_execution_table(cpu_history, cycles):
    print("".ljust(8), end="")
    for i in range(cycles):
        print(f"C{i+1}".center(10), end="")
    print()
    for cpu_name in sorted(cpu_history):
        print(cpu_name.ljust(8), end="")
        for entry in cpu_history[cpu_name]:
            print(entry.center(10), end="")
        print()

def main():
    tasks = [
        {"id": "T1", "quantum": 10, "requiredCpus": 1, "totalDuration": 40},
        {"id": "T2", "quantum": 20, "requiredCpus": 2, "totalDuration": 20},
        {"id": "T3", "quantum": 10, "requiredCpus": 2, "totalDuration": 30},
        {"id": "T4", "quantum": 15, "requiredCpus": 1, "totalDuration": 40},
        {"id": "T5", "quantum": 15, "requiredCpus": 1, "totalDuration": 30},
        {"id": "T6", "quantum": 20, "requiredCpus": 4, "totalDuration": 60},
        {"id": "T7", "quantum": 10, "requiredCpus": 1, "totalDuration": 20},
        {"id": "T8", "quantum": 20, "requiredCpus": 2, "totalDuration": 40},
        {"id": "T9", "quantum": 15, "requiredCpus": 2, "totalDuration": 50},
        {"id": "T10", "quantum": 10, "requiredCpus": 4, "totalDuration": 60},
    ]

    cpus = initialize_cpus(4)
    tasks = initialize_tasks(tasks)
    cpu_history = create_cpu_history(cpus)
    run_scheduler(tasks, cpus, cpu_history)
    cycles = fill_cpu_history(cpu_history)
    print_execution_table(cpu_history, cycles)

if __name__ == "__main__":
    main()