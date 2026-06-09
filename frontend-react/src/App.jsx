import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000/analyze";

const COLOR_SWATCHES = {
  Warm: ["#808000", "#C7942F", "#C66B3D", "#E8B04B", "#F4A77B", "#FFF1D6"],
  Cool: ["#0F6E5C", "#1F4E8C", "#7B2D5E", "#5B6B8C", "#C0C6CC", "#FFFFFF"],
  Neutral: ["#8A7E72", "#B7A99A", "#D8CEC2", "#9C9388", "#EDE7DE", "#FBF8F3"],
};

function App() {
  const [faceFile, setFaceFile] = useState(null);
  const [bodyFile, setBodyFile] = useState(null);
  const [facePreview, setFacePreview] = useState(null);
  const [bodyPreview, setBodyPreview] = useState(null);
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const pickFace = (e) => {
    const f = e.target.files[0];
    setFaceFile(f);
    setFacePreview(f ? URL.createObjectURL(f) : null);
  };

  const pickBody = (e) => {
    const f = e.target.files[0];
    setBodyFile(f);
    setBodyPreview(f ? URL.createObjectURL(f) : null);
  };

  const handleAnalyze = async () => {
    if (!faceFile || !bodyFile) {
      setStatus("Please choose both a face photo and a body photo.");
      setResult(null);
      return;
    }

    setStatus("");
    setLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append("face", faceFile);
    formData.append("body", bodyFile);

    try {
      const response = await fetch(API_URL, { method: "POST", body: formData });
      const data = await response.json();
      if (data.error) {
        setStatus("Error: " + data.error);
      } else {
        setResult(data);
      }
    } catch (err) {
      setStatus("Could not reach the server. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  const swatches = result ? COLOR_SWATCHES[result.undertone] || [] : [];

  return (
    <div className="page">
      <div className="grain" />

      <header className="hero">
        <p className="eyebrow">AI Personal Styling</p>
        <h1 className="title">
          Style <span className="title-accent">&amp;</span> Glow
        </h1>
        <p className="subtitle">
          Upload two photos. We read your undertone and silhouette, then curate
          a wardrobe palette, flattering cuts, and a makeup look made for you.
        </p>
      </header>

      <main className="studio">
        <section className="uploads">
          <UploadCard
            index="01"
            label="The Face"
            hint="A clear, well-lit close-up"
            preview={facePreview}
            onChange={pickFace}
          />
          <UploadCard
            index="02"
            label="The Form"
            hint="Full body, standing, facing forward"
            preview={bodyPreview}
            onChange={pickBody}
          />
        </section>

        <button className="cta" onClick={handleAnalyze} disabled={loading}>
          {loading ? "Reading your portrait…" : "Curate my look"}
        </button>

        {status && <p className="status">{status}</p>}

        {result && (
          <section className="results">
            <div className="result-head">
              <Stat label="Undertone" value={result.undertone} />
              <Stat
                label="Silhouette"
                value={result.body_shape}
                sub={`ratio ${result.ratio}`}
              />
            </div>

            <div className="panel reveal" style={{ animationDelay: "0.05s" }}>
              <h3 className="panel-title">Your Palette</h3>
              <div className="swatch-row">
                {swatches.map((hex, i) => (
                  <span
                    key={i}
                    className="swatch"
                    style={{ background: hex, animationDelay: `${0.1 + i * 0.05}s` }}
                  />
                ))}
              </div>
              <ul className="list">
                {result.colors.map((c, i) => <li key={i}>{c}</li>)}
              </ul>
            </div>

            <div className="panel reveal" style={{ animationDelay: "0.15s" }}>
              <h3 className="panel-title">Cuts &amp; Silhouettes</h3>
              <ul className="list">
                {result.cuts.map((c, i) => <li key={i}>{c}</li>)}
              </ul>
            </div>

            {result.makeup && (
              <div className="panel reveal" style={{ animationDelay: "0.25s" }}>
                <h3 className="panel-title">Your Makeup Look</h3>
                <div className="makeup-grid">
                  <MakeupCard title="Lipstick" items={result.makeup.lipstick} />
                  <MakeupCard title="Blush" items={result.makeup.blush} />
                  <MakeupCard title="Eyeshadow" items={result.makeup.eyeshadow} />
                </div>
              </div>
            )}
          </section>
        )}
      </main>

      <footer className="foot">Built with FastAPI · MediaPipe · React</footer>
    </div>
  );
}

function UploadCard({ index, label, hint, preview, onChange }) {
  return (
    <label className="card">
      <span className="card-index">{index}</span>
      <div className="card-preview">
        {preview ? <img src={preview} alt={label} /> : <span className="card-placeholder">+</span>}
      </div>
      <span className="card-label">{label}</span>
      <span className="card-hint">{hint}</span>
      <input type="file" accept="image/*" onChange={onChange} hidden />
    </label>
  );
}

function MakeupCard({ title, items }) {
  return (
    <div className="makeup-card">
      <span className="makeup-title">{title}</span>
      <ul className="makeup-list">
        {(items || []).map((it, i) => <li key={i}>{it}</li>)}
      </ul>
    </div>
  );
}

function Stat({ label, value, sub }) {
  return (
    <div className="stat">
      <span className="stat-label">{label}</span>
      <span className="stat-value">{value}</span>
      {sub && <span className="stat-sub">{sub}</span>}
    </div>
  );
}

export default App;