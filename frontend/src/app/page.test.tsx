import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import TodoPage from "./page";
import { apiClient } from "@/lib/api-client";

vi.mock("@/lib/api-client", () => ({
  apiClient: {
    listTodos: vi.fn(),
    createTodo: vi.fn(),
    updateTodo: vi.fn(),
    deleteTodo: vi.fn(),
  },
}));

vi.mock("sonner", () => ({
  toast: {
    error: vi.fn(),
    success: vi.fn(),
  },
}));

const mockedApi = vi.mocked(apiClient);

const todo = {
  id: 7,
  title: "Ship the todo app",
  completed: false,
  created_at: "2026-01-01T00:00:00Z",
  updated_at: "2026-01-01T00:00:00Z",
};

describe("TodoPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockedApi.listTodos.mockResolvedValue([]);
  });

  it("shows loading and then the empty state", async () => {
    let resolveList: (value: typeof todo[]) => void = () => undefined;
    mockedApi.listTodos.mockReturnValue(new Promise((resolve) => {
      resolveList = resolve;
    }));
    render(<TodoPage />);
    expect(screen.getByText("Loading shared tasks...")).toBeInTheDocument();
    resolveList([]);
    expect(await screen.findByText("No tasks yet.")).toBeInTheDocument();
  });

  it("submits a new task and clears the form", async () => {
    mockedApi.createTodo.mockResolvedValue(todo);
    render(<TodoPage />);
    await screen.findByText("No tasks yet.");
    const input = screen.getByTestId("todo-form-title");
    fireEvent.change(input, { target: { value: "Ship the todo app" } });
    fireEvent.submit(screen.getByRole("button", { name: "Add task" }).closest("form") as HTMLFormElement);
    expect(mockedApi.createTodo).toHaveBeenCalledWith({ title: "Ship the todo app" });
    expect(await screen.findByText("Ship the todo app")).toBeInTheDocument();
    expect(input).toHaveValue("");
  });

  it("toggles completion and confirms deletion before removing a task", async () => {
    mockedApi.listTodos.mockResolvedValue([todo]);
    mockedApi.updateTodo.mockResolvedValue({ ...todo, completed: true });
    mockedApi.deleteTodo.mockResolvedValue(undefined);
    render(<TodoPage />);
    await screen.findByText(todo.title);
    fireEvent.click(screen.getByTestId("todo-toggle-7"));
    await waitFor(() => expect(mockedApi.updateTodo).toHaveBeenCalledWith(7, { completed: true }));
    fireEvent.click(screen.getByTestId("todo-delete-7"));
    expect(await screen.findByText("Delete this task?")).toBeInTheDocument();
    fireEvent.click(screen.getByTestId("todo-delete-confirm"));
    await waitFor(() => expect(mockedApi.deleteTodo).toHaveBeenCalledWith(7));
    expect(screen.queryByText(todo.title)).not.toBeInTheDocument();
  });

  it("renders API errors and supports retry", async () => {
    mockedApi.listTodos.mockRejectedValueOnce(new Error("Unable to load tasks."));
    mockedApi.listTodos.mockResolvedValueOnce([]);
    render(<TodoPage />);
    expect(await screen.findByTestId("todo-error-banner")).toHaveTextContent("Unable to load tasks.");
    fireEvent.click(screen.getByTestId("todo-error-retry"));
    expect(await screen.findByText("No tasks yet.")).toBeInTheDocument();
  });
});