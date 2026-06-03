import ConversationList from "./ConversationList";
import MessagePanel from "./MessagePanel";

export default function ChatLayout() {
  return (
    <div style={styles.container}>
      <aside style={styles.sidebar}>
        <ConversationList />
      </aside>

      <main style={styles.main}>
        <MessagePanel />
      </main>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    display: "flex",
    height: "100vh",
    width: "100vw",
    overflow: "hidden",
  },
  sidebar: {
    width: "280px",
    borderRight: "1px solid #ddd",
    padding: "12px",
  },
  main: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
  },
};