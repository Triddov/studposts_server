//пользовательский fetch
async function MakeRequest(url, params) {
    try {
        //выполнение запроса
        const response = await fetch(url, params);

        //ошибки верхнего уровня
        if (!response.ok) {
            const error = new Error("Внутренняя ошибка");
            error.status = response.status;
            error.message = response.statusText;
            throw error;
        }

        //получение внутренних данных
        const data = await response.json();

        //внутренние ошибки
        if (data.status >= 400) {
            console.log('Make Req', data);
            throw Object.assign(new Error(), data);
        }

        //данные ответа
        return data;

    //блок обработки ошибок
    } catch (err) {

        //для ошибок сети
        if (!err.status) {
            throw Object.assign(new Error(), {
                message: "Проверьте подключение к интернету",
                status: "Ошибка сети"
            });
        }

        //для ошибок со статусом
        throw err;
    }
}

//экспорт
export default MakeRequest;
