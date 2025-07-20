export default function SimplePage() {
  return (
    <div style={{ 
      padding: '20px', 
      fontFamily: 'Arial, sans-serif',
      backgroundColor: '#f0f0f0',
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center'
    }}>
      <h1>Simple Test Page</h1>
      <p>Next.js is working!</p>
      <p>Time: {new Date().toLocaleString()}</p>
    </div>
  );
} 