module.exports = {
  networks: {
    development: {
      host: "127.0.0.1",
      port: 7545,         // Ganache GUI default RPC port
      network_id: "5777", // Ganache GUI network ID
    },
  },

  compilers: {
    solc: {
      version: "0.8.19", // match your contract pragma
      settings: {
        optimizer: {
          enabled: true,
          runs: 200
        }
      }
    }
  }
};
