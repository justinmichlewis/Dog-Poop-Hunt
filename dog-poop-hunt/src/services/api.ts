const deletePoop = async (poopId: number, pickedUserId: number) => {
  const currentDate = new Date();
  const formattedDate = currentDate.toISOString().split("T")[0];

  const myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  const raw = JSON.stringify({
    state: "completed",
    completedDate: formattedDate,
    pickedUserId: pickedUserId,
  });

  const requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: raw,
    redirect: "follow",
  };
  return await fetch(
    "http://127.0.0.1:5000/api/poops/" + poopId,
    requestOptions
  )
    .then((response) => response.text())
    .then((result) => {
      console.log(result);
      return result;
    })
    .catch((error) => {
      return error;
    });
};

export { deletePoop };
