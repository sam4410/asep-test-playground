"use client";

import { FormEvent, useEffect, useState } from "react";
import { AlertCircle, CheckCircle2, Loader2, Plus, Trash2, X } from "lucide-react";
import { toast } from "sonner";
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle } from "@/components/ui/alert-dialog";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { apiClient, Todo } from "@/lib/api-client";
import "../styles/design-tokens.css";
import "./todo.css";

export default function TodoPage() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [busyId, setBusyId] = useState<number | null>(null);
  const [error, setError] = useState("");
  const [deleting, setDeleting] = useState<Todo | null>(null);

  async function loadTodos() {
    setLoading(true);
    setError("");
    try {
      setTodos(await apiClient.listTodos());
    } catch (caught) {
      const message = caught instanceof Error ? caught.message : "Unable to load tasks.";
      setError(message);
      toast.error(message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadTodos();
  }, []);

  async function addTodo(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const value = title.trim();
    if (!value || saving) {
      return;
    }
    setSaving(true);
    setError("");
    try {
      const todo = await apiClient.createTodo({ title: value });
      setTodos((items) => [...items, todo]);
      setTitle("");
      toast.success("Task added.");
    } catch (caught) {
      const message = caught instanceof Error ? caught.message : "Unable to add task.";
      setError(message);
      toast.error(message);
    } finally {
      setSaving(false);
    }
  }

  async function toggleTodo(todo: Todo) {
    setBusyId(todo.id);
    try {
      const updated = await apiClient.updateTodo(todo.id, { completed: !todo.completed });
      setTodos((items) => items.map((item) => item.id === updated.id ? updated : item));
      toast.success(updated.completed ? "Task completed." : "Task reopened.");
    } catch (caught) {
      const message = caught instanceof Error ? caught.message : "Unable to update task.";
      setError(message);
      toast.error(message);
    } finally {
      setBusyId(null);
    }
  }

  async function removeTodo() {
    if (!deleting) {
      return;
    }
    const todo = deleting;
    setBusyId(todo.id);
    try {
      await apiClient.deleteTodo(todo.id);
      setTodos((items) => items.filter((item) => item.id !== todo.id));
      setDeleting(null);
      toast.success("Task deleted.");
    } catch (caught) {
      const message = caught instanceof Error ? caught.message : "Unable to delete task.";
      setError(message);
      toast.error(message);
    } finally {
      setBusyId(null);
    }
  }

  const completed = todos.filter((todo) => todo.completed).length;

  return (
    <main className="page-shell">
      <Card className="todo-card">
        <CardHeader className="page-header">
          <div>
            <p className="eyebrow">SHARED TASK STREAM</p>
            <CardTitle className="page-title">Todo list</CardTitle>
            <p className="subtitle">A focused list for everyone.</p>
          </div>
          <Badge variant="outline">{completed}/{todos.length} done</Badge>
        </CardHeader>
        <CardContent>
          <form className="add-form" onSubmit={addTodo}>
            <Input data-testid="todo-form-title" value={title} onChange={(event) => setTitle(event.target.value)} placeholder="Add a task and press Enter" aria-label="Task title" maxLength={500} disabled={saving} />
            <Button data-testid="todo-form-submit" type="submit" disabled={saving || !title.trim()}><Plus size={17} />{saving ? "Adding..." : "Add task"}</Button>
          </form>
          {error && <div data-testid="todo-error-banner" className="error-banner" role="alert"><AlertCircle size={18} /><span>{error}</span><Button data-testid="todo-error-retry" variant="outline" size="sm" onClick={() => void loadTodos()}>Retry</Button></div>}
          {loading ? (
            <div className="state-message"><Loader2 className="animate-spin" size={24} /><span>Loading shared tasks...</span></div>
          ) : todos.length === 0 ? (
            <div className="state-message"><CheckCircle2 size={30} /><strong>No tasks yet.</strong><span>Add the first task to get the shared list moving.</span></div>
          ) : (
            <ul className="task-list" aria-label="Shared tasks">
              {todos.map((todo) => (
                <li data-testid={`todo-card-${todo.id}`} className={`task-row ${todo.completed ? "is-complete" : ""}`} key={todo.id}>
                  <Checkbox data-testid={`todo-toggle-${todo.id}`} checked={todo.completed} disabled={busyId === todo.id} onCheckedChange={() => void toggleTodo(todo)} aria-label={`Mark ${todo.title} ${todo.completed ? "incomplete" : "complete"}`} />
                  <span className="task-title">{todo.title}</span>
                  <Badge variant={todo.completed ? "secondary" : "outline"}>{todo.completed ? "done" : "open"}</Badge>
                  <Button data-testid={`todo-delete-${todo.id}`} variant="ghost" size="icon" disabled={busyId === todo.id} onClick={() => setDeleting(todo)} aria-label={`Delete ${todo.title}`}><Trash2 size={17} /></Button>
                </li>
              ))}
            </ul>
          )}
        </CardContent>
      </Card>
      <AlertDialog open={Boolean(deleting)} onOpenChange={(open) => !open && setDeleting(null)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Delete this task?</AlertDialogTitle>
            <AlertDialogDescription>{deleting ? `"${deleting.title}" will be removed from the shared list.` : ""}</AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel data-testid="todo-delete-cancel"><X size={16} />Keep task</AlertDialogCancel>
            <AlertDialogAction data-testid="todo-delete-confirm" onClick={() => void removeTodo()}><Trash2 size={16} />Delete task</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </main>
  );
}
