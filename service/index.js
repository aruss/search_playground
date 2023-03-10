"use strict";

const Hapi = require("@hapi/hapi");
const spawn = require("child_process").spawn;

async function search(term) {
  return new Promise((resolve, reject) => {
    const child = spawn("python", ["search.py", term, "json"]);

    let data = "";

    child.stdout.on("data", (chunk) => {
      data += chunk;
    });

    child.stdout.on("end", () => {
      try {
        console.log("parsing data", data);
        const result = JSON.parse(data);
        resolve(result);
      } catch (error) {
        reject(error);
      }
    });

    child.on("error", (error) => {
      reject(error);
    });

    child.on("close", (code) => {
      if (code !== 0) {
        reject(new Error(`child process exited with code ${code}`));
      }
    });
  });
}

function getSearchTerm(request) {
  const q = request.query["q"];
  if (q) {
    return q.replace(/[^a-z\d ]+/gi, "");
  }
}

const init = async () => {
  const server = Hapi.server({
    port: 3000,
    host: "localhost",
  });

  await server.register(require("@hapi/vision"));

  server.views({
    engines: {
      html: require("handlebars"),
    },
    relativeTo: __dirname,
    path: "templates",
    helpersPath: "helpers",
  });

  server.route({
    method: "GET",
    path: "/api",
    handler: async (request, h) => {
      const term = getSearchTerm(request);

      // if no term provided return empty result
      if (!term) {
        return h
          .response({
            message:
              "provide search term by setting q query parameter ?q=your_search_term",
          })
          .code(400);
      }

      const searchResult = await search(term);

      return h
        .response({
          term: term,
          items: searchResult,
        })
        .code(200);
    },
  });

  server.route({
    method: "GET",
    path: "/",
    handler: async (request, h) => {
      
      return h.view('index');
    },
  });

  await server.start();
  console.log("Server running on %s", server.info.uri);
};

process.on("unhandledRejection", (err) => {
  console.log(err);
  process.exit(1);
});

init();
