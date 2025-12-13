"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { motion } from "framer-motion";
import axios from "axios";
import { SandpackProvider, SandpackPreview, SandpackCodeEditor, SandpackLayout } from "@codesandbox/sandpack-react";

export default function CodeGeneratorMock() {
  const [prompt, setPrompt] = useState("");
  const [showLists, setShowLists] = useState(false);
  const [outline, setOutline] = useState<{ sectionName: string; description: string }[]>([]);
  const [newSection, setNewSection] = useState<{ sectionName: string; description: string }>({ sectionName: "", description: "" });
  const [loading, setLoading] = useState(false);
  const [files, setFiles] = useState<Record<string, string>>({});
  const [selectedFile, setSelectedFile] = useState<string>("");
  const [showPreview, setShowPreview] = useState(true);

  const handleSubmit = async () => {
    if (prompt.trim() !== "") {
      setLoading(true);
      setShowLists(false);
      setOutline([]);
      try {
        const res = await fetch(` http://127.0.0.1:8000/generate-outline/?topic=${encodeURIComponent(prompt)}`, {
          method: "GET",
          headers: { "Content-Type": "application/json" },
        
        });
        const data = await res.json();
        if (Array.isArray(data.outline)) {
          setOutline(data.outline);
          setShowLists(true);
        }
      } catch (err) {
        console.error("Error fetching outline:", err);
      } finally {
        setLoading(false);
      }
    }
  };

  const handleEnter = async (e: any) => {
    if (e.key === "Enter") {
      await handleSubmit();
    }
  };

  const addSection = () => {
    if (newSection.sectionName.trim() !== "" && newSection.description.trim() !== "") {
      setOutline([...outline, newSection]);
      setNewSection({ sectionName: "", description: "" });
    }
  };

  const fetchPreview = async () => {
    try {
      setLoading(true);
      const res = await fetch("http://127.0.0.1:8000/generate-code", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ outline }),
      });
      const data = await res.json();
      console.log("Received data:", data);
      if (data && data.files) {
        setFiles(data.files);
        const firstFile = Object.keys(data.files)[0];
        setSelectedFile(firstFile);
      }
    } catch (error) {
      console.error("Error fetching preview:", error);
      alert("Failed to generate code. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const downloadZip = async () => {
    try {
      const JSZip = (await import("jszip")).default;
      const zip = new JSZip();
      
      Object.entries(files).forEach(([path, code]) => {
        zip.file(path, code);
      });
      
      const blob = await zip.generateAsync({ type: "blob" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "generated-app.zip";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Error creating zip:", error);
      alert("Failed to download files.");
    }
  };

  return (
    <div className="min-h-screen bg-linear-to-br from-gray-50 to-gray-100 flex flex-col items-center justify-center py-10 px-4">
      
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-800 mb-2">Auto-UI Generator</h1>
        <p className="text-gray-600">Describe your website and we'll create an outline for you</p>
      </div>

      {/* ChatGPT-style centered input with send button */}
      <div className="max-w-2xl w-full">
        <div className="flex gap-2 items-center">
          <Input
            placeholder="Describe your website idea..."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyDown={handleEnter}
            disabled={loading}
            className="text-lg py-6 shadow-lg border-2 focus:border-blue-500 transition-all"
          />
          <Button 
            onClick={handleSubmit}
            disabled={loading || prompt.trim() === ""}
            size="lg"
            className="px-8 py-6 shadow-lg"
          >
            {loading ? "Generating..." : "Send"}
          </Button>
        </div>
      </div>

      {/* Outline Lists */}
      {showLists && outline.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-12 w-full max-w-4xl"
        >
          <Card className="shadow-xl border-2">
            <CardHeader className="bg-linear-to-r from-blue-50 to-indigo-50">
              <CardTitle className="text-2xl text-center">Website Outline</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3 p-6">
              {outline.map((item, i) => (
                <div key={i} className="p-4 bg-linear-to-r from-gray-50 to-gray-100 rounded-lg border border-gray-200 hover:shadow-md transition-shadow">
                  <strong className="text-blue-600">{item.sectionName}</strong>
                  <p className="text-gray-700 mt-1">{item.description}</p>
                </div>
              ))}

              <div className="flex flex-col gap-2 mt-6 pt-6 border-t">
                <p className="text-sm font-semibold text-gray-600 mb-2">Add Custom Section</p>
                <Input
                  placeholder="Section name…"
                  value={newSection.sectionName}
                  onChange={(e) => setNewSection({ ...newSection, sectionName: e.target.value })}
                  className="border-2"
                />
                <Input
                  placeholder="Description…"
                  value={newSection.description}
                  onChange={(e) => setNewSection({ ...newSection, description: e.target.value })}
                  className="border-2"
                />
                <Button onClick={addSection} className="mt-2">Add Section</Button>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      )}

      {/* Generate Code Button */}
      {showLists && outline.length > 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="mt-8 mb-10"
        >
          <Button
          onClick={() => fetchPreview()}
           size="lg" className="px-12 py-7 text-lg shadow-xl bg-linear-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700">
            Generate Code
          </Button>
        </motion.div>
      )}

      {loading && <p className="mt-4 text-gray-500">Generating outline...</p>}

      {/* Code Preview */}
      {Object.keys(files).length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-12 w-full max-w-7xl mb-10"
        >
          <Card className="shadow-xl border-2">
            <CardHeader className="bg-linear-to-r from-blue-50 to-indigo-50">
              <div className="flex items-center justify-between w-full">
                <CardTitle className="text-2xl">Generated Code</CardTitle>
                <div className="flex gap-2">
                  <Button 
                    onClick={() => setShowPreview(!showPreview)}
                    variant={showPreview ? "default" : "outline"}
                    size="sm"
                  >
                    {showPreview ? "Show Code" : "Show Preview"}
                  </Button>
                  <Button onClick={downloadZip} className="bg-green-600 hover:bg-green-700" size="sm">
                    Download ZIP
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent className="p-6">
              {showPreview ? (
                <div className="w-full h-[700px]">
                  <SandpackProvider 
                    template="react"
                    files={files}
                    theme="dark"
                  >
                    <SandpackLayout>
                      <SandpackPreview 
                        showNavigator={false}
                        showRefreshButton={true}
                        showOpenInCodeSandbox={false}
                      />
                    </SandpackLayout>
                  </SandpackProvider>
                </div>
              ) : (
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
                  {/* File Browser */}
                  <div className="lg:col-span-1 border rounded-lg p-4 bg-gray-50 max-h-[600px] overflow-y-auto">
                    <h3 className="font-semibold mb-3 text-gray-700">Files</h3>
                    <div className="space-y-1">
                      {Object.keys(files).map((filePath) => (
                        <button
                          key={filePath}
                          onClick={() => setSelectedFile(filePath)}
                          className={`w-full text-left px-3 py-2 rounded text-sm transition-colors ${
                            selectedFile === filePath
                              ? "bg-blue-100 text-blue-700 font-medium"
                              : "hover:bg-gray-200 text-gray-700"
                          }`}
                        >
                          {filePath}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Code Viewer */}
                  <div className="lg:col-span-2 border rounded-lg bg-gray-900 p-4 max-h-[600px] overflow-auto">
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-gray-300 text-sm font-mono">{selectedFile}</span>
                      <button
                        onClick={() => {
                          navigator.clipboard.writeText(files[selectedFile]);
                          alert("Copied to clipboard!");
                        }}
                        className="text-xs bg-gray-700 hover:bg-gray-600 text-white px-3 py-1 rounded"
                      >
                        Copy
                      </button>
                    </div>
                    <pre className="text-sm text-gray-100 font-mono overflow-x-auto">
                      <code>{files[selectedFile]}</code>
                    </pre>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </motion.div>
      )}
    </div>
  );
}
