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
    redirect: "follow",
  };

  return await fetch("http://127.0.0.1:5000/api/poops", requestOptions)
    .then((response) => response.json())
    .then((result) => {
      return { success: true, res: result };
    })
    .catch((error) => {
      return { success: false, res: error };
    });
};

const getPoops = async () => {
  return await fetch("http://127.0.0.1:5000/api/poops")
    .then((response) => response.json())
    .then((data) => {
      return { success: true, res: data };
    })
    .catch((error) => {
      return { success: false, res: error };
    });
};

const getUser = async (userName: string) => {
  return await fetch("http://127.0.0.1:5000/api/users/" + userName)
    .then((response) => response.json())
    .then((data) => {
      return data;
    })
    .catch((error) => {
      console.log(error);
    });
};

const getAchievements = async (userName: string) => {
  return await fetch("http://127.0.0.1:5000/api/achievements/" + userName)
    .then((response) => response.json())
    .then((data) => {
      return data;
    })
    .catch((error) => {
      console.log(error);
    });
};

export { deletePoop, createPoop, getPoops, getUser, getAchievements };
