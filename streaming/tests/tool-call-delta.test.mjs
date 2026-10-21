import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import test from "node:test";
import { parse } from "cddl";

const schema = parse(fileURLToPath(new URL("../protocol.cddl", import.meta.url)));

test("tool-call-delta requires a string slice and extends the delta union", () => {
  const delta = schema.find(({ Name }) => Name === "ToolCallDelta");
  const type = delta.Properties.find(({ Name }) => Name === "type");
  const args = delta.Properties.find(({ Name }) => Name === "args");
  assert.equal(type.Type[0].Value, "tool-call-delta");
  assert.deepEqual(args.Type, ["text"]);
  assert.deepEqual(args.Occurrence, { n: 1, m: 1 });
  assert.ok(delta.Properties.some(({ Type }) => Type[0]?.Value === "Extensible"));
  const union = schema.find(({ Name }) => Name === "ContentBlockDelta");
  assert.deepEqual(union.PropertyType.map(({ Value }) => Value), [
    "TextDelta", "ReasoningDelta", "DataDelta", "BlockDelta", "ToolCallDelta",
  ]);
});

test("documented tool-call deltas reconstruct the final argument object", () => {
  const readme = readFileSync(new URL("../README.md", import.meta.url), "utf8");
  const section = readme.split("#### Append-only tool-call arguments")[1];
  const events = JSON.parse(section.match(/```json\n([\s\S]*?)\n```/)[1]);
  for (const event of events) {
    assert.equal(event.event, "content-block-delta");
    assert.equal(event.index, 1);
    assert.equal(event.delta.type, "tool-call-delta");
    assert.equal(typeof event.delta.args, "string");
  }
  assert.deepEqual(JSON.parse(events.map(({ delta }) => delta.args).join("")), {
    query: "weather",
  });
});
