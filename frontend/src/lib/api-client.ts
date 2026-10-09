export type Todo = {
  id: number;
  title: string;
  completed: boolean;
  created_at?: string;
  updated_at?: string;
};

export type CreateTodoRequest = {
  title: string;
};

export type UpdateTodoRequest = {
  title?: string;
  completed?: boolean;
};

const TODO_PATH = "/api/v1/todos";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    ...init,
    headers: {
      Accept: "application/json",      "Content-Type": "application/json",
      ...init?.headers,
    },
  });
  if (!response.ok) {
    let message = `Request failed with status ${response.status}`;
    try {
      const body = (await response.json()) as { detail?: string };
      if (body.detail) {
        message = body.detail;
      }
    } catch {
      message = `Request failed with status ${response.status}`;
    }
    throw new Error(message);
  }
  if (response.status === 204) {
    return undefined as T;
  }
  return (await response.json()) as T;
}

export const apiClient = {
  listTodos: () => request<Todo[]>(TODO_PATH),
  createTodo: (payload: CreateTodoRequest) =>
    request<Todo>(TODO_PATH, {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  updateTodo: (id: number, payload: UpdateTodoRequest) =>
    request<Todo>(`${TODO_PATH}/${id}`, {
      method: "PATCH",
      body: JSON.stringify(payload),
    }),
  deleteTodo: (id: number) =>
    request<void>(`${TODO_PATH}/${id}`, {
      method: "DELETE",
    }),
};
