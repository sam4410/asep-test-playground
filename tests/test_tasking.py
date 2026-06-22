from __future__ import annotations

import pytest
from uuid import uuid4
from asep.domain import Task
from asep.tasking import resolve_execution_order

def test_resolve_execution_order_simple():
    t1 = Task(title="T1", description="", owner="pm")
    t2 = Task(title="T2", description="", owner="pm", dependencies=[t1.id])
    t3 = Task(title="T3", description="", owner="pm", dependencies=[t2.id])
    
    tasks = [t3, t2, t1]
    order = resolve_execution_order(tasks)
    
    assert order == [t1.id, t2.id, t3.id]

def test_resolve_execution_order_circular():
    t1 = Task(title="T1", description="", owner="pm")
    t2 = Task(title="T2", description="", owner="pm", dependencies=[t1.id])
    
    # Introduce cycle: t1 depends on t2
    t1.dependencies.append(t2.id)
    
    with pytest.raises(ValueError, match="Task graph contains a cycle"):
        resolve_execution_order([t1, t2])

def test_resolve_execution_order_unknown_dependency():
    t1 = Task(title="T1", description="", owner="pm", dependencies=[uuid4()])
    
    with pytest.raises(ValueError, match="depends on unknown task"):
        resolve_execution_order([t1])
