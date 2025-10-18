// constants.js
export const getTypeColor = (type) => {
    switch (type) {
        case "ЛK":
            return "geekblue";
        case "ПР":
            return "cyan";
        case "ЛАБ":
            return "magenta";
        default:
            return "gray";
    }
};

export const getStatusColor = (status) => {
    switch (status) {
        case "Н":
            return "red";
        case "+":
            return "green";
        case "У":
            return "gray";
        default:
            return "red";
    }
};
