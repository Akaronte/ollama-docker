import { useState } from "react";
import ReactMarkdown from "react-markdown";
import { postText } from "./api";
import styles from "./App.module.css";

export default function App() {
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [responseBody, setResponseBody] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    setErrorMessage("");
    setResponseBody(null);

    try {
      const data = await postText(inputValue);
      setResponseBody(data);
    } catch (error) {
      setErrorMessage(error.message ?? "Error desconocido");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className={styles.container}>
      <section className={styles.card}>
        <h1 className={styles.title}>LLM con búsqueda integrada</h1>
        <p className={styles.subtitle}>
          LLM con capacidad de búsqueda integrada
        </p>

        <form className={styles.form} onSubmit={handleSubmit}>
          <input
            className={styles.input}
            id="text-input"
            type="text"
            value={inputValue}
            onChange={(event) => setInputValue(event.target.value)}
            placeholder="Ollama con search api"
            required
            autoComplete="off"
          />
          <button className={styles.button} type="submit" disabled={isLoading}>
            {isLoading ? "Enviando..." : "Enviar"}
          </button>
        </form>

        {errorMessage && <p className={styles.error}>Error: {errorMessage}</p>}

        {responseBody?.summary && (
          <section className={styles.summary}>
            <h2>Resumen</h2>
            <ReactMarkdown>{responseBody.summary}</ReactMarkdown>
          </section>
        )}

        {responseBody && (
          <section className={styles.response}>
            <h2>Respuesta completa</h2>
            <pre>{JSON.stringify(responseBody, null, 2)}</pre>
          </section>
        )}
      </section>
    </main>
  );
}
