import time
import pytest


@pytest.mark.parametrize("iterations", [20])
def test_workspace_create_delete_performance(client, iterations):
    """
    Simple performance sanity check: repeatedly create and delete a workspace.
    The test ensures that a modest number of operations complete within an
    acceptable time bound, confirming that workspace isolation does not cause
    severe degradation under load.
    """
    start = time.time()
    for i in range(iterations):
        # Create a new workspace
        create_resp = client.post(
            "/workspaces",
            json={"name": f"perf-test-{i}"},
        )
        assert create_resp.status_code == 201, "Workspace creation failed"
        ws_id = create_resp.json()["id"]

        # Delete the workspace
        delete_resp = client.delete(f"/workspaces/{ws_id}")
        assert delete_resp.status_code == 204, "Workspace deletion failed"

    duration = time.time() - start
    # Arbitrary threshold; adjust based on CI performance expectations
    assert duration < 5.0, f"Performance test exceeded time limit: {duration:.2f}s"