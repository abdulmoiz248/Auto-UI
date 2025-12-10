"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { motion } from "framer-motion";

export default function CodeGeneratorMock() {
  const [prompt, setPrompt] = useState("");
  const [showLists, setShowLists] = useState(false);

  const [pages, setPages] = useState(["Home Page", "Login Page"]);
  const [instructions, setInstructions] = useState(["Use Tailwind", "Use clean folder structure"]);

  const [newPage, setNewPage] = useState("");
  const [newInstruction, setNewInstruction] = useState("");

  const handleEnter = (e: any) => {
    if (e.key === "Enter" && prompt.trim() !== "") {
      setShowLists(true);
    }
  };

  const addPage = () => {
    if (newPage.trim() !== "") {
      setPages([...pages, newPage]);
      setNewPage("");
    }
  };

  const addInstruction = () => {
    if (newInstruction.trim() !== "") {
      setInstructions([...instructions, newInstruction]);
      setNewInstruction("");
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

      {/* Suggested Lists */}
      {showLists && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-12 grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-5xl"
        >
          {/* Suggested Pages */}
          <Card className="shadow-lg">
            <CardHeader>
              <CardTitle>Suggested Pages</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {pages.map((p, i) => (
                <div key={i} className="p-2 bg-gray-100 rounded-lg">
                  {p}
                </div>
              ))}

              <div className="flex gap-2 mt-3">
                <Input
                  placeholder="Add page…"
                  value={newPage}
                  onChange={(e) => setNewPage(e.target.value)}
                />
                <Button onClick={addPage}>Add</Button>
              </div>
            </CardContent>
          </Card>

          {/* Key Instructions */}
          <Card className="shadow-lg">
            <CardHeader>
              <CardTitle>Key Instructions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {instructions.map((p, i) => (
                <div key={i} className="p-2 bg-gray-100 rounded-lg">
                  {p}
                </div>
              ))}

              <div className="flex gap-2 mt-3">
                <Input
                  placeholder="Add instruction…"
                  value={newInstruction}
                  onChange={(e) => setNewInstruction(e.target.value)}
                />
                <Button onClick={addInstruction}>Add</Button>
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
    </div>
  );
}
