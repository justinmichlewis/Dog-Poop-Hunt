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
  };
  return await fetch(
    "http://127.0.0.1:8000/api/poops/" + poopId,
    requestOptions
  )
    .then((response) => response.text())
    .then((result) => {
      return { success: true, res: result };
    })
    .catch((error) => {
      return { success: false, res: error };
    });
};

const createPoop = async (
  description: string,
  userId: number,
  latitude: Number,
  longitude: Number
) => {
  const currentDate = new Date();
  const formattedDate = currentDate.toISOString().split("T")[0];

  const myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  const raw = JSON.stringify({
    latitude: latitude,
    longitude: longitude,
    description: description,
    state: "active",
    placedUserId: userId,
    pickedUserId: null,
    createdDate: formattedDate,
    completedDate: null,
  });

  const requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: raw,
  };

  return await fetch("http://127.0.0.1:8000/api/poops", requestOptions)
    .then((response) => response.json())
    .then((result) => {
      return { success: true, res: result };
    })
    .catch((error) => {
      return { success: false, res: error };
    });
};

const getPoops = async () => {
  return await fetch("http://127.0.0.1:8000/api/poops")
    .then((response) => response.json())
    .then((data) => {
      return { success: true, res: data };
    })
    .catch((error) => {
      return { success: false, res: error };
    });
};

const authenticateUser = async (email: string, password: object) => {
  const raw = JSON.stringify({
    email: email,
    password: password,
  });

  const myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  const requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: raw,
  };

  return await fetch(
    "http://127.0.0.1:8001/api/users/authenticate",
    requestOptions
  )
    .then((response) => response.json())
    .then((result) => {
      return result;
    })
    .catch((error) => {
      return error;
    });
};

const getAchievements = async (userId: number) => {
  return await fetch("http://127.0.0.1:8000/api/achievements/" + userId)
    .then((response) => response.json())
    .then((data) => {
      return data;
    })
    .catch((error) => {
      console.log(error);
    });
};

export { deletePoop, createPoop, getPoops, getAchievements, authenticateUser };
