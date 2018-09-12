import random

def get_idxs(rat, gauge_set, test_probs, valid_prob, seed = 101):
    
    random.seed(seed)

    n = len(rat.index)
    testnum = int(n*test_probs[2])
    validnum = int(n*valid_prob)
    
    user_ids = set(rat['user_id'].unique())
    joke_ids = set(rat['joke_id'].unique()) - set(gauge_set)
    test_user_ids = random.sample(user_ids, int(len(user_ids)*test_probs[0]))
    test_joke_ids = random.sample(joke_ids, int(len(joke_ids)*test_probs[1]))
    
    user_flag = rat['user_id'].isin(test_user_ids)
    joke_flag = rat['joke_id'].isin(test_joke_ids)

    test_nuser_idxs = set(rat.index[user_flag & -joke_flag])
    test_njoke_idxs = set(rat.index[-user_flag & joke_flag])
    test_nuser_njoke_idxs = set(rat.index[user_flag & joke_flag])

    remainder = set(rat.index) - test_nuser_idxs - test_njoke_idxs - test_nuser_njoke_idxs
    test_idxs = set(random.sample(remainder, testnum))
    remainder = remainder - test_idxs
    valid_idxs = set(random.sample(remainder, validnum))
    train_idxs = remainder - valid_idxs
    
    assert set(rat.index) == train_idxs.union(valid_idxs, test_idxs, test_nuser_idxs,
                                          test_njoke_idxs, test_nuser_njoke_idxs)
    
    return (sorted(train_idxs), sorted(valid_idxs), sorted(test_idxs),
           sorted(test_nuser_idxs), sorted(test_njoke_idxs), 
           sorted(test_nuser_njoke_idxs))