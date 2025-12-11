"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { motion } from "framer-motion";

export default function CodeGeneratorMock() {
  const [prompt, setPrompt] = useState("");
  const [showLists, setShowLists] = useState(false);
  const [outline, setOutline] = useState<{ sectionName: string; description: string }[]>([]);
  const [newSection, setNewSection] = useState<{ sectionName: string; description: string }>({ sectionName: "", description: "" });
  const [loading, setLoading] = useState(false);

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
          <Button size="lg" className="px-12 py-7 text-lg shadow-xl bg-linear-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700">
            Generate Code
          </Button>
        </motion.div>
      )}

      {loading && <p className="mt-4 text-gray-500">Generating outline...</p>}
    </div>
  );
}
