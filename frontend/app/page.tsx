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

  const handleEnter = async (e: any) => {
    if (e.key === "Enter" && prompt.trim() !== "") {
      setLoading(true);
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

  const addSection = () => {
    if (newSection.sectionName.trim() !== "" && newSection.description.trim() !== "") {
      setOutline([...outline, newSection]);
      setNewSection({ sectionName: "", description: "" });
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center py-10 px-4">
      
      {/* ChatGPT-style centered input */}
      <div className="max-w-xl w-full mt-24">
        <Input
          placeholder="Ask anything…"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          onKeyDown={handleEnter}
          className="text-lg py-6 shadow-md"
        />
      </div>

      {/* Outline Lists */}
      {showLists && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-12 grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-5xl"
        >
          <Card className="shadow-lg">
            <CardHeader>
              <CardTitle>Website Outline</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {outline.map((item, i) => (
                <div key={i} className="p-2 bg-gray-100 rounded-lg">
                  <strong>{item.sectionName}</strong>: {item.description}
                </div>
              ))}

              <div className="flex flex-col gap-2 mt-3">
                <Input
                  placeholder="Section name…"
                  value={newSection.sectionName}
                  onChange={(e) => setNewSection({ ...newSection, sectionName: e.target.value })}
                />
                <Input
                  placeholder="Description…"
                  value={newSection.description}
                  onChange={(e) => setNewSection({ ...newSection, description: e.target.value })}
                />
                <Button onClick={addSection}>Add Section</Button>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      )}

      {/* Generate Code Button */}
      {showLists && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="mt-10"
        >
          <Button size="lg" className="px-10 py-6 text-lg shadow-xl">
            Generate Code
          </Button>
        </motion.div>
      )}

      {loading && <p className="mt-4 text-gray-500">Generating outline...</p>}
    </div>
  );
}
